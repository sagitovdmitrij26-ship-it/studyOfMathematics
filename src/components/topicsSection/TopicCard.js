import "./TopicCard.css";
/* Карточка с темой */
function TopicCard({ topic }) {
    const { id, image, title, number, numberOfTopics, actions } = topic; /* деструктуризация объекта topic */
    return (
<div className="card">
    <img src={image} alt={title}></img> {/* Добавляем иконку в карточку */}
    <h3>{title}</h3>  {/* Добавляем заголовок в карточку */} 
    <span>{number} {numberOfTopics}</span> {/* Добавляем класс и количество уроков в карточку */}
    <p>{actions}</p> {/* Добавляем описание в карточку */}
        <div className="raiting">{/* Добавим в карточку уровень освоения материала по теме */}
        <h4>Освоено:</h4>
        {/* добавим в карточку уровень освоения материала в процентах и шкале и кнопку начать тему
        путем вкладывания новой функции в функцию TopicCard*/}
        
        </div>
</div>
    )
}

export default TopicCard;