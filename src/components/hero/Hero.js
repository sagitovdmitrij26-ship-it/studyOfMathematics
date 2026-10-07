import "./Hero.css";

function Hero({ onStart }) {
  return (
    <div className="wrap">
      {" "}
      {/* Wrap для центрирования контента */}
      <div className="hero">
        {" "}
        {/* Контейнер для контента */}
        <div className="heroCopy">
          {" "}
          {/* Контейнер для левой части контента */}
          <div className="heroBadge">
            {" "}
            {/* Контейнер для пояснения назначения сайта */}
            <span></span>
            <h4>Онлайн-тренажёр для 5-8 классов</h4>
          </div>
          <h1>Математика, которая наконец становится понятной</h1>
          <div className="heroSub">
            <p>
              Короткая теория, пошаговые разборы и мгновенная проверка. Тренажёр
              покажет, где именно вы ошиблись и что стоит <br /> повторить.
            </p>
          </div>
          {/* Кнопки для начала тренажерa и просмотра программы */}
          <div className="heroCta">
            {/* левая кнопка для начала тренажерa */}
            <button className="btnStart" onClick={onStart}>
              Начать бесплатно <img src="/image/arrow-right.png" alt="Sigma" />
            </button>
            {/* правая кнопка для просмотра программы */}
            <button className="btnProgram">
              {" "}
              <img src="/image/play.svg" alt="Sigma" /> Смотреть программу
            </button>
          </div>
        </div>
        {/* Контейнер для правой части контента (образец рабочей части) */}
        <div className="heroVisual">
          {/* Верхняя часть блока */}
          <div className="prewiewTop">
            <div className="topicChip">Алгебра: 8 класс</div>
            <p>Задача 4 из 10</p>
          </div>
          <p>            
            Решите уравнение: x<sup>2</sup> - 5x + 6 = 0
          </p>
          <div className="formulaBlock">
            D = b <sup>2</sup> - 4ac = 25 - 24 = 1
          </div>
        
        </div>
      </div>
    </div>
  );
}

export default Hero;
