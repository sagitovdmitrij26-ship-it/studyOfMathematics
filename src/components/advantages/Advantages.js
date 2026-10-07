/* Блок с преимуществами тренажора по математике */
/* Подключим компонент AdvantagesCard одной карточки */
import AdvantagesCard from "./AdvantagesCard";
import "./Advantages.css"; /* подключаем стили */

function Advantages(props) {
  const {advantages = []} = props;
  return (
    <div className="wrap">
      {" "}
        {/* Верхняя часть блока============================================================ */}
      <div className="advantagesHeader">        
        <h3>Преимущества</h3>
        <h2>Почему с тренажёром получается?</h2>
        <p>
          Мы убрали то, что мешает школьникам: длинную теорию, страх ошибки и
          отсутствие обратной связи.
        </p>
      </div>
      {/* Нижняя часть блока============================================================== */}
      <div className="advantagesFooter">
{advantages.length ? advantages.map((advantage) => (
  <AdvantagesCard key={advantage.id} advantage={advantage} />
)) : null}
      </div>
    </div>
  );
}

export default Advantages;
