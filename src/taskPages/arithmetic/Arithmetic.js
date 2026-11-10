import "./Arithmetic.css";
import { useEffect, useState } from "react";
import { supabase } from "../../supabaseClient";

function Arithmetic() {
    /* tasks — массив задач, который увидит JSX. Сначала он пустой, страница рисуется без списка */
    /* setTasks — функция, которой мы потом положим ответ из базы; после этого React перерисует компонент */
    const [tasks, setTasks] = useState([]);
    /* Для проверки введенного пользователем ответа напишем useState */
    const [answer, setAnswer] = useState("");
    /* напишем еще useState для результата проверки */
    const [result, setResult] = useState("");

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
            const { data, error } = await supabase
                .from("tasks") /* какую таблицу читать (имя как в Dashboard) */
                .select("*") /* какие колонки взять; * = все колонки строки */
                .eq("subject", "arithmetic") /* фильтр: только строки, где subject равен arithmetic */
                .order("id"); /* сортировка по id, чтобы задачи шли по порядку */

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
        };

        /* Объявить fetchTasks мало: React сам её не запустит. Вызов отправляет запрос */
        fetchTasks();
        /* [] — список зависимостей. Пустой = выполнить эффект один раз, когда открыли страницу */
        /* Если [] убрать, после каждого setTasks эффект запустится снова и будет бесконечно спрашивать базу */
    }, []);

    /* currentIndex — номер задачи в массиве: 0 это первая, 1 вторая и т.д. */
    /* Массив уже упорядочен по id в .order("id"), поэтому индекс 0 = задача с меньшим id */
    const [currentIndex, setCurrentIndex] = useState(0);

    /* tasks — массив, у него нет поля id. id есть у одной строки: tasks[0], tasks[1]... */
    const task = tasks[currentIndex];

    /* Функция проверки введенного ответа. Следующая задача — только если ответ верный */
    function checkAnswer() {
        /* Сначала проверяем, ввёл ли ученик текст. Это поле answer из useState, не колонка таблицы */
        if (!answer.trim()) {
            return;
        }

        const user = answer.trim();
        const correct = String(task.answer ?? "").trim();

        if (user === correct) {
            setResult("Правильно!");
            setAnswer("");
            /* Не выходим за последнюю задачу */
            if (currentIndex < tasks.length - 1) {
                setCurrentIndex(currentIndex + 1);
                setResult("");
            }
        } else {
            setResult("Неправильно!");
        }
    }

    return (
        <div className="wrap">
            <div className="wrapper">
                {
                    /* Пока tasks пустой (загрузка или нет строк), task равен undefined — рисуем заглушку */
                    task ? (
                        <div className="current-task">
                            {/* Здесь task.id — номер строки из таблицы, не индекс массива */}
                            <h2>Задача №{task.id}</h2>
                            {task.image ? <img src={task.image} alt="" /> : null}
                            <p>{task.question}</p>

                            <div className="answer-buttons">
                                <input
                                    type="text"
                                    placeholder="Введите ответ"
                                    value={answer}
                                    onChange={(e) => setAnswer(e.target.value)}
                                />
                                <button type="button" onClick={checkAnswer}>
                                    Проверить ответ
                                </button>
                            </div>
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
