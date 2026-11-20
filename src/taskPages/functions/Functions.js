import "./Functions.css";
import { useState } from "react";
import ResultTopic from "../resultTopic/ResultTopic";
import useTasks from "../useTasks";
import topics from "../../topic.json";

function Functions() {
    /* useTasks — загрузка задач из Supabase. Хуки вызываются только внутри компонента */
    const { tasks, selectedClass, selectedLevel } = useTasks("function");
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
                explanation: task.explanation_of_the_answer,
                image: task.image,
                id: task.id
            }
        ])
        /* Не выходим за последнюю задачу */
        if (currentIndex < tasks.length - 1) {
            setCurrentIndex(currentIndex + 1);
            setResult("");
        } else {
            setShowResult(true);
        }
    }
    /* создадим переменную которая будет содержать текущую тему */
    let catalogTopicList; /* создали переменную снаружи от if чтобы она
     была доступна в любом месте функции */
    if (topics.catalogTopicLists[3].title === "Функции") {
        catalogTopicList = topics.catalogTopicLists[2];
    }


    /* =======================================функция проверки введенного ответа============================================= */
    /* Итог возвращаем отдельно: иначе он остаётся внутри .wrapper и фон снова сужается до 1280px */
    if (showResult) {
        return (
            <ResultTopic
                listAnswers={listAnswers}
                catalogTopicList={catalogTopicList}
                selectedClass={selectedClass}
                selectedLevel={selectedLevel}
                onRepeat={() => {
                    setShowResult(false);
                    setCurrentIndex(0);
                    setListAnswers([]);
                    setAnswer("");
                    setResult("");
                }}
            />
        );
    }
/* напишем условие, что если будет выбрано 5-6 класс на любом уровне сложно то будет выведена надпись "В №класса эту тему еще не
изучают" */
if (selectedClass === "5–6 класс" ) {
    return (
        <div className='wrap'>
            <div className='wrapper'>
                <div className='no-tasks'>
                    <span className="no-tasks__badge">Функции</span>
                    <h1>В {selectedClass}е эту тему ещё не изучают</h1>
                    <p>Линейные и квадратичные функции появляются с 7 класса. Выберите другой класс в каталоге — тренажёр подстроит задания под уровень.</p>
                </div>
            </div>
        </div>
    )
}
    return (
        < div className="wrap" >
            <div className="wrapper">
                {
                    /* Пока tasks пустой (загрузка или нет строк), task равен undefined — рисуем заглушку */
                    task ? (
                        <div className="current-task">
                            {/* Номер в сессии: 1, 2, 3… не id строки в Supabase */}
                            <h2>Задача №{currentIndex + 1}</h2>
                            {task.image ? (
                                <img className="task-figure" src={task.image} alt={task.question} />
                            ) : (
                                <p>{task.question}</p>
                            )}
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
                            {result ? <h3>{result}</h3> : null}
                        </div>
                    ) : (
                        <h3>Задачи пока не загрузились</h3>
                    )
                }
            </div>
        </div >
    )
}

export default Functions;

