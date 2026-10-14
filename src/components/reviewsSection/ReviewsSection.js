/* блок "отзывы" о сайте */
import "./ReviewsSection.css";

function ReviewsSection({ rewiews = [] }) {
  return (
    <div className="wrap">
      <div className="wrapper">
        {/* ================================== шапка блока============================ */}
        <div className="reviewsHeader">
          <h3>Отзывы</h3>
          <h2>Ученики и родители о тренажёре</h2>
          <p>Собрали отзывы за последний учебный год.</p>
        </div>
        {/* ======================================подвал блока======================== */}
        <div className="rewiewsFooter">
          {
            rewiews.length
            ? rewiews.map((rewiew) => <)
          }
        </div>
        {/* ========================================================================== */}
      </div>
    </div>
  );
}
export default ReviewsSection;
