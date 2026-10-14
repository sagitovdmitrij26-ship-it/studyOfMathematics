import PathCard from "./PathCard";
/* Подключим стили для этого блока */
import "./LeaningPath.css";

/* Функция для этого блока */
function LeaningPath({ paths = [] }) {
  return (    
    <div className="leaningSection">
      <div className="wrap">
        <div className="wrapper">      

          {/* шапка текущего блока */}
          {/* ======================================================== */}
          <div className="LeaningHead">
            <h3>Как проходит обучение</h3>
            <h2>Путь от пробелов до уверенных решений</h2>
            <p>
              Четыре шага повторяются в каждой теме — вы всегда знаете, что
              делать дальше.
            </p>
          </div>
          {/* ======================================================== */}
          <div className="pathFooter">
            {paths.length
              ? paths.map((path) => <PathCard key={path.id} path={path} />)
              : null}
          </div>
          {/* ======================================================== */}
        </div>
      </div>
    </div>
  );
}

export default LeaningPath;
