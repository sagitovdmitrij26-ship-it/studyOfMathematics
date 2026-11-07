import "./CatalogTopicCard.css";

function CatalogTopicCard({ catalogTopicList, activeClass }) {
    /* деструктуризация объекта catalogTopicList из файла topic.json */
    const { id, image, title, numberOfTopics, actions } = catalogTopicList;
    return (
        <div className='catalog-topic-card'> {/* полоса (карточка) с предметом */}
            <img src={image} alt={title}></img> {/* изображение предмета */}
            <div className="card-explanation"> {/* блок внутри карточки с названием и описанием */}
                <h3>{title}</h3> {/* название предмета */}
                <p>{actions}</p> {/* описание предмета (что включает в себя предмет) */}
            </div>
            <div className='progress-bar'>
                <span>{activeClass || "Выберите класс"}</span>
            </div>
            <button>Открыть раздел</button>
        </div>

    )
}
export default CatalogTopicCard;
