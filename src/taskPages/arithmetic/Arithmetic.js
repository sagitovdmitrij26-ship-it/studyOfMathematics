import "./Arithmetic.css";
import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom"; /* хук React Router: читает хвост ссылки после ? */
import { supabase } from "../../supabaseClient";

function Arithmetic() {
    /* ============================хуки для сайта==================================================================*/
    /* Пример ссылки: /Arithmetic?class=5–6 класс&level=Базовый — её собрал CatalogTopicCard при клике «Открыть раздел» */
    /* useSearchParams возвращает объект с методами get/set. Нам нужен только get — читать, не менять */
    const [searchParams] = useSearchParams();
    /* get("class") берёт значение параметра class. Имя должно совпасть с тем, что в search у navigate */
    /* Если открыли /Arithmetic без хвоста, get вернёт null — тогда фильтр по классу/уровню ниже не применится */
    const selectedClass = searchParams.get("class");
    const selectedLevel = searchParams.get("level");
    /* tasks — массив задач, который увидит JSX. Сначала он пустой, страница рисуется без списка */
    /* setTasks — функция, которой мы потом положим ответ из базы; после этого React перерисует компонент */
    const [tasks, setTasks] = useState([]);
    /* Для проверки введенного пользователем ответа напишем useState */
    const [answer, setAnswer] = useState("");
    /* напишем еще useState для результата проверки */
    const [result, setResult] = useState("");
    /* currentIndex — номер задачи в массиве: 0 это первая, 1 вторая и т.д. */
    /* Массив уже упорядочен по id в .order("id"), поэтому индекс 0 = задача с меньшим id */
    const [currentIndex, setCurrentIndex] = useState(0);
    /* создадим состояние для результатов решения задач, т.к. ниже в функции checkAnswer состояние о прошлых результатах
    не остается, а просто получает новый результат от новой задачи.*/
    const [listAnswers, setListAnswers] = useState([]);
    /* Напишем еще одно состояние для перехода на страницу ResultTopic после решения всех задач */
    const [showResult, setShowResult] = useState(false);
   

    /* useEffect — «сделай это после отрисовки». Запрос к базе нельзя писать прямо в теле функции: она должна быстро вернуть JSX */
    useEffect(() => {
        /* async — помечает функцию: внутри можно ждать сервер через await, не блокируя весь сайт */
        const fetchTasks = async () => {
            /* supabase берётся из supabaseClient.js. Если нет URL/ключа в .env.local, там null */
            /* return — выходим из функции, запрос не отправляем, иначе будет ошибка */
            if (!supabase) {
                return;
            }

            /* await — ждём ответ. Без него data ещё не будет готова */
            /* { data, error } — из ответа сразу достаём два поля: массив строк и ошибку */
            /* query собираем по шагам: сначала предмет, потом при необходимости класс и уровень */
            /* let, не const — ниже к цепочке дописываем .eq, переменную нужно перезаписать */
            let query = supabase
                .from("arithmetic_tasks") /* новая таблица с теми же колонками, что у tasks */
                .select("*") /* какие колонки взять; * = все колонки строки */
                .eq("subject", "arithmetic"); /* фильтр: только строки, где subject равен arithmetic */

            /* .eq(колонка, значение) = «оставь строки, где колонка точно равна значению» */
            /* Имена колонок class_name и level — как в Table Editor, не как в каталоге (там пропсы activeClass / isDifficultyLevel) */
            /* Текст значения должен совпасть с кнопкой: «5–6 класс», «Базовый». «базовый» или «5-6» не подойдут */
            if (selectedClass) {
                query = query.eq("class_name", selectedClass);
            }
            if (selectedLevel) {
                query = query.eq("level", selectedLevel);
            }

            /* order в конце цепочки: сортировка уже отфильтрованного набора по id */
            const { data, error } = await query.order("id");

            /* error будет, если нет таблицы, нет колонки или RLS не даёт SELECT */
            /* return — не вызываем setTasks, чтобы не затереть состояние битым ответом */
            if (error) {
                console.log(error); /* смотрите сообщение в консоли браузера (F12) */
                return;
            }

            /* data — уже массив задач с сервера */
            /* ?? [] — если data вдруг null, кладём пустой массив, чтобы потом можно было писать tasks.map */
            /* setTasks запоминает массив и заставляет React нарисовать страницу заново уже с задачами */
            setTasks(data ?? []);
            /* Новый набор задач (другой класс/уровень) — начинаем с первой, иначе currentIndex может указать мимо массива */
            setCurrentIndex(0);
            setAnswer(""); /* поле ответа от прошлой задачи не должно остаться */
            setResult(""); /* «Правильно!» / «Неправильно!» тоже сбрасываем */
            setShowResult(false); /* состояние для перехода на страницу ResultTopic после решения всех задач */
            setListAnswers([]); /* очищаем массив ответов для нового набора задач */
        };

        /* Объявить fetchTasks мало: React сам её не запустит. Вызов отправляет запрос */
        fetchTasks();
        /* Второй аргумент useEffect — зависимости. Раньше был []: загрузить один раз при входе на страницу */
        /* Теперь в массиве selectedClass и selectedLevel: если в ссылке сменились класс или уровень, эффект запустится снова */
        /* Сами setTasks сюда не ставим — иначе после каждого ответа базы эффект крутился бы бесконечно */
    }, [selectedClass, selectedLevel]);    
 /* ============================================================================================================================*/
    /* tasks — массив, у него нет поля id. id есть у одной строки: tasks[0], tasks[1]... */
    const task = tasks[currentIndex];
/* =======================================функция проверки введенного ответа============================================= */
    /* Функция проверки введенного ответа. */
    function checkAnswer() {
        /* Сначала проверяем, ввёл ли ученик текст. Это поле answer из useState, не колонка таблицы */
        if (!answer.trim()) {
            return;
        }

        const user = answer.trim();
        const correct = String(task.answer ?? "").trim();

        if (user === correct) {
            setResult("Правильно!");        
            
        } else {
            setResult("Неправильно!");
        }
        /* Теперь нужно добавить введенный ответ в массив listAnswers, чтобы сохранить ответ и на другие задачи */
        setListAnswers((prev) => [
            ...prev,
            {
                question: task.question,
                userAnswer: user,
                correctAnswer: correct,
                isCorrect: user === correct,
                explanation: task.explanation,
                image: task.image,
            }
        ])
        /* Не выходим за последнюю задачу */
            if (currentIndex < tasks.length - 1) {
                setCurrentIndex(currentIndex + 1);
                setResult("");
            } else{
                setShowResult(true);
            }
    }
/* =======================================функция проверки введенного ответа============================================= */
    return (
        <div className="wrap">
            <div className="wrapper">
                {
                    /* Пока tasks пустой (загрузка или нет строк), task равен undefined — рисуем заглушку */
                    task ? (
                        <div className="current-task">
                            {/* Здесь task.id — номер строки из таблицы, не индекс массива */}
                            <h2>Задача №{task.id}</h2>
                            <p>{task.question}</p>
                            <div className="answer-buttons">
                                <input
                                    type="text"
                                    placeholder="Введите ответ"
                                    value={answer}
                                    onChange={(e) => setAnswer(e.target.value)}
                                />
                                <button
                                    type="button"
                                    onClick={checkAnswer}
                                >
                                    Проверить ответ
                                </button>
                            </div>
                            {task.image ? <img src={task.image} alt="" /> : null}
                            {result ? <h3>{result}</h3> : null}
                        </div>
                    ) : (
                        <h3>Задачи пока не загрузились</h3>
                    )
                }
            </div>
        </div>
    );
}

export default Arithmetic;

