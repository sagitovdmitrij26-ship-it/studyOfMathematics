import "./ResultTopic.css";


function ResultTopic({ listAnswers, catalogTopicList, selectedClass, selectedLevel }) {
    /* создадим переменную которая будет содержать название раздела */
    let nameTopic = "";
    let numberClass = "";
    if (catalogTopicList && catalogTopicList.title === "Арифметика") {
        nameTopic = catalogTopicList.title;
        numberClass = selectedClass || "";
    }
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
                {/* блок в котором будут 2 блока (правильные и неправильные ответы) */}
                <div className="correct_incorrect_answers">
                    <div className='correct_answers'>
                        <h3>Количество правильных ответов:</h3>


                    </div>
                    <div className='incorrect_answers'>
                        <h3>Количество неправильных ответов:</h3>


                    </div>
                </div>
            </div>
        </div>
    )
}
export default ResultTopic;