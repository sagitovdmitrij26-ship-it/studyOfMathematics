import TopicCard from "./TopicCard";
/* Импорт стилей css для этого компонента */
import "./TopicsSection.css";

/* Напишем функциональный элемент с общими темами */
function TopicsSection(props) {
  const {topics = []} = props
  return (
    <div className="wrap">
      <div className="topicSection">
        {/* ====================================================================== */}
        <div className="topicsHead">
          {" "}
          {/* верхняя часть блока */}
          <h3>Популярные темы</h3>
          <h2>Начните с темы, где нужен прорыв</h2>
          <p>
            Каждая тема разбита на короткие уроки: теория, разборы и практика.
            Прогресс считается автоматически.
          </p>
        </div>
        {/* ====================================================================== */}
        <div className="topicCards"> {/* Карточки с разными темами */}
           {topics.length ? topics.map((topic) => (
           <TopicCard key={topic.id} topic={topic} />
           ))
           : <h3>No topics found</h3>}

        </div>
        {/* ====================================================================== */}
      </div>
    </div>
  );
}

export default TopicsSection;
