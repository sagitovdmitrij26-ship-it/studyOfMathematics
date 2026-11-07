import { useState } from "react";
import Entrance from "../../homePage/entrance/entrance";
import Logo from "../logoSite/Logo";
import "./Header.css";
import {Link} from "react-router-dom";

function Header({ onForm, onSignUp }) {
  const [isOpen, setIsOpen] = useState(false);

  const handleToggle = () => {
    setIsOpen(!isOpen);
  
  };
  return (
    <header className="header">
      <div className="wrap">
        <div className="wrapper"> {/* блок внутри для размера 1280px */}
          {/* Передаём логотип и название как children в компонент Entrance */}
          <Entrance>
            <div className="image">
              <Logo />
            </div>
          </Entrance>
          <nav>
            <ul>
              <li><Link to="/">Главная</Link></li>
              <li>Курс</li>
              <li><Link to="/CatalogTopics">Темы</Link></li>
              <li>Об авторе</li>
              <li>Отзывы</li>
              <li>Цены</li>
            </ul>
          </nav>
          <div className="action">
            <button className="logIn" onClick={onForm}>
              Войти
            </button>
            <button className="signUp" onClick={ onSignUp }>Записаться</button>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;
