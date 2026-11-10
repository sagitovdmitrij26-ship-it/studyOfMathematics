import { useNavigate } from "react-router-dom";
import "./CatalogTopicCard.css";

function CatalogTopicCard({ catalogTopicList, activeClass, isDifficultyLevel }) {
    /* деструктуризация объекта catalogTopicList из файла topic.json */
    const { id, image, title, numberOfTopics, actions } = catalogTopicList;
    const navigate = useNavigate();
    /* цвет фона бейджа в зависимости от уровня сложности */
    let badgeColor = "#e8eaf2"; /* Зададим цвет по умолчаю, пока не выбран уровень сложности */
    if (isDifficultyLevel === "Базовый") {/* если выбран базовый уровень */
        badgeColor = "#d4f5d9"; /* зеленый цвет */
    } else if (isDifficultyLevel === "Средний") { /* если выбран средний уровень */
        badgeColor = "#fff3c4"; /* желтый цвет */
    } else if (isDifficultyLevel === "Высокий") { /* если выбран высокий уровень */
        badgeColor = "#ffd8c2"; /* красный цвет */
    }
    return (
        <div className='catalog-topic-card'> {/* полоса (карточка) с предметом */}
            <img src={image} alt={title}></img> {/* изображение предмета */}
            <div className="card-explanation"> {/* блок внутри карточки с названием и описанием */}
                <div className="card-explanation__title">
                    <h3>{title}</h3> {/* название предмета */}
                    <span style={{ backgroundColor: badgeColor, borderRadius: "15px", padding: "8px 20px", fontWeight: "600"}}>{isDifficultyLevel || "Выберите уровень сложности"}</span>
                </div>
                <p>{actions}</p> {/* описание предмета (что включает в себя предмет) */}
            </div>
            <div className='progress-bar'>
                <span>{activeClass || "Выберите класс"}</span>
            </div>
            <button type="button" onClick={() => navigate("/Arithmetic")}>Открыть раздел</button>
        </div>

    )
}
export default CatalogTopicCard;
