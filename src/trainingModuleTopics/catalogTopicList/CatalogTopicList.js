import CatalogTopicCard from "./CatalogTopicCard";
import "./CatalogTopicList.css";

function CatalogTopicList({ catalogTopicLists = [], activeClass, isDifficultyLevel }) {
    return (
        <div className="wrap">
            <div className="wrapper">
                <div className="catalogTopicList">
                    {
                        catalogTopicLists.length ? (
                            catalogTopicLists.map((catalogTopicList) =>
                            <CatalogTopicCard
                                key={catalogTopicList.id}
                                catalogTopicList={catalogTopicList}
                                activeClass={activeClass}
                                isDifficultyLevel={isDifficultyLevel}
                            />)
                        ) : (
                            <h3>No catalog topic lists found</h3>
                        )
                    }
                </div>
            </div>
        </div>
    )
}
export default CatalogTopicList;