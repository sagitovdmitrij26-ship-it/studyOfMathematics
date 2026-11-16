import "./ResultTopic.css";
import { useNavigate } from "react-router-dom"; /* импортируем useNavigate для перехода на другую страницу */


function ResultTopic({ listAnswers, catalogTopicList, selectedClass, selectedLevel, onRepeat }) {
    const navigate = useNavigate(); /* создаем переменную navigate для перехода на другую страницу */
    /* создадим переменную которая будет содержать название раздела */
    let nameTopic = "";
    let numberClass = "";
    if (catalogTopicList && catalogTopicList.title) {
        nameTopic = catalogTopicList.title;
        numberClass = selectedClass || "";
    }
    /* listAnswers содержит все ответы которые дал пользователь. Из этого массива можно выбрать правильные ответы и потом 
    найти неправильные отняв из всех задач правильные ответы */
    const correctAnswers = listAnswers.filter((answer) => answer.isCorrect) /* переменная, где хранятся правильные ответы, полученные из
    массива методом filter */
    const inCorrectAnswers = listAnswers.filter((answer) => !answer.isCorrect)
    /* переменная где хроанятся неправильные ответы. Их получаем применив метод filter
    только используем только те ответы, которые не являются правильными */


    return (
        /* resultTopic снаружи: у него нет max-width, фон идёт на всю ширину окна */
        <div className="resultTopic">
            <div className="wrap">
                <div className="wrapper">
                    {/* создание бэйджика  для показа раздела, класса, уровня сложности*/}
                    <div className="name_tag">
                        {nameTopic}
                        {numberClass ? ` · ${numberClass}` : ""}
                        {selectedLevel ? ` · ${selectedLevel}` : ""}
                    </div>
                    <h2>Результаты решения задач по теме с пояснениями</h2>
                    <h3>Все задачи раздела решены. Ниже верные ответы и пояснения к ним.</h3>
                </div>
                {/* =================================================вывод количества правильных и неправильных ответов==================================== */}
                {/* блок в котором будут 2 блока (правильные и неправильные ответы) */}
                <div className="correct_incorrect_answers">
                    <div className='correct_answers'>
                        <h3>Количество правильных ответов:</h3>
                        <span>{correctAnswers.length}</span> {/* длина массива правильных ответов */}

                    </div>
                    <div className='incorrect_answers'>
                        <h3>Количество неправильных ответов:</h3>
                        <span>{inCorrectAnswers.length}</span> {/* длина массива неправильных ответов */}

                    </div>
                </div>
                {/* ================================================================================================================ */}
                {/* ==========================================вывод таблицы с результатами============================================= */}
                <div className='table_answers'>
                    <table>
                        <thead>
                            <tr>
                                {/* Шапка таблицы с названием каждой колонки */}
                                <th>№</th>
                                <th>Задача</th>
                                <th>Ваш ответ</th>
                                <th>Верный</th>
                                <th>Пояснение</th>
                            </tr>
                        </thead>
                        <tbody>
                            {listAnswers.map((answer, index) => (
                                <tr key={answer.id ?? index}>
                                    <td>{index + 1}</td>
                                    <td>{answer.question}</td>
                                    <td>
                                        <span className={answer.isCorrect ? "answer_correct" : "answer_wrong"}>
                                            {answer.userAnswer}
                                        </span>
                                    </td>
                                    <td>
                                        <span className="answer_correct">{answer.correctAnswer}</span>
                                    </td>
                                    <td>{answer.explanation}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
                {/* ================================================================================================================ */}
                {/* ========================================кнопки для дальнейших действий=========================================== */}
                <div className='buttons'>
                    <button
                        className='repeat_tasks'
                        type="button"
                        onClick={onRepeat}
                    >
                        Повторить решение задач
                    </button>
                    <button
                        className='back_to_topics'
                        type="button"
                        onClick={() => navigate("/catalogTopics")}
                    >
                        Назад к темам
                    </button>
                </div>
                {/* ================================================================================================================= */}
            </div>
        </div>
    )
}
export default ResultTopic;