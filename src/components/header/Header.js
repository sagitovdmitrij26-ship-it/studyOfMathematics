
import { useState } from "react";
import Entrance from "../entrance/entrance";
import "./Header.css";

function Header({ onForm }) {
  const [isOpen, setIsOpen] = useState(false);

  const handleToggle = () => {
    setIsOpen(!isOpen);
  };
  return (
    <header className="header">
      <div className="wrap">
        {/* Передаём логотип и название как children в компонент Entrance */}
        <Entrance>
          <div className="image">

            <img src="/image/sigma.svg" alt="Sigma" />
            <h3>Матеум</h3>

          </div>
        </Entrance>
        <nav>
          <ul>
            <li>Главная</li>
            <li>Курс</li>
            <li>Темы</li>
            <li>Об авторе</li>
            <li>Отзывы</li>
            <li>Цены</li>
          </ul>
        </nav>
        <div className="action">
          <button className="logIn" onClick={onForm}>Войти</button>
          <button className="signUp">Записаться</button>
        </div>
      </div>
    </header>
  );
}

export default Header;
