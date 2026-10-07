/* Создадим форму карточки в данном блоке */
/* Подключаем стили одной карточки */
import "./AdvantagesCard.css"

function AdvantagesCard({ advantage }) {
    const { image, title, text, path } = advantage
    return (
        <div className="advantagesCard">
            <img src={image} alt={title} />
            <h3>{title}</h3>
            <p>{text}</p>
            <span>{path}</span>
            
        </div>
    )

}

export default AdvantagesCard;