import "./Arithmetic.css";
import { useState } from "react";
import ResultTopic from "../resultTopic/ResultTopic";
import useTasks from "../useTasks";
/* импортируем массив с темами topics чтобы передать в ResultTopic */
import  topics  from "../../topic.json";

function Arithmetic() {
    /* useTasks — загрузка задач из Supabase. Хуки вызываются только внутри компонента */
    const { tasks, selectedClass, selectedLevel } = useTasks("arithmetic");
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
    if (topics.catalogTopicLists[0].title === "Арифметика") {
        catalogTopicList = topics.catalogTopicLists[0];
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

    return (
        < div className="wrap" >
            <div className="wrapper">
                {
                        /* Пока tasks пустой (загрузка или нет строк), task равен undefined — рисуем заглушку */
                        task ? (
                            <div className="current-task">
                                {/* Номер в сессии: 1, 2, 3… не id строки в Supabase */}
                                <h2>Задача №{currentIndex + 1}</h2>
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
        </div >
    );
}

export default Arithmetic;
