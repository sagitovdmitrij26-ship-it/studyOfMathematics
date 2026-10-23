import "./Footer.css"; /* Стили для футера */
import { Link } from "react-router-dom"; /* Для перехода по ссылкам */
import Logo from "../logoSite/Logo"; /* Логотип сайта */
import Icons from "../icons/Icons"; /* Иконки для футера */


function Footer() {
    return (
        <footer className="footer">
            <div className="wrap">
                <div className="wrapper">
                    {/* Верхняя часть футера */}
                    <div className="footerTop">
                        <div className="footerLogo">
                            <Logo />
                            <p>Тренажёр по математике для 5–11 классов: теория, разборы и практика с мгновенной проверкой.</p>
                            {/* ====================блок с социальными сетями======================= */}
                            <div className="socialMedia">
                                <Icons name="telegram" alt="telegram"
                                    style={{
                                        width: "30px", height: "30px",
                                        cursor: "pointer"
                                    }} />
                                <Icons name="max" alt="max" style={{
                                    width: "30px", height: "30px",
                                    cursor: "pointer"
                                }} />
                            </div>
                        </div>
                        {/* ===========блок с разделами======================= */}
                        <div className="footerCol">
                            <h3>Разделы</h3>
                            <ul>
                                <li><Link to="/">Арифметика</Link></li>
                                <li><Link to="/">Алгебра</Link></li>
                                <li><Link to="/">Геометрия</Link></li>
                                <li><Link to="/">Функции и графики</Link></li>
                                <li><Link to="/">Текстовые задачи</Link></li>
                            </ul>
                        </div>
                        {/* ===========блок обучение======================= */}
                        <div className="footerCol">
                            <h3>Обучение</h3>
                            <ul>
                                <li><Link to="/">Программа курса</Link></li>
                                <li><Link to="/">Учителя</Link></li>
                                <li><Link to="/">Тренажёр задач</Link></li>
                                <li><Link to="/">Отзывы</Link></li>
                                <li><Link to="/">Цены</Link></li>
                            </ul>
                        </div>
                        {/* ===========блок контакты======================= */}
                        <div className="footerCol">
                            <h3>Помощь</h3>
                            <ul>
                                <li><Link to="/">Частые вопросы</Link></li>
                                <li><a href="mailto:hello@mateum.ru">hello@mateum.ru</a></li>
                                <li><a href="tel:+74951204567">+7 495 120-45-67</a></li>
                                <li><Link to="/">Поддержка учеников</Link></li>
                            </ul>

                        </div>
                    </div>
                    <div className="footerBottom">
                        <p className="footerCopy">© 2025 Матеум. Все права защищены.</p>
                        <div className="footerSymbols">
                            <span>π</span>
                            <span>Σ</span>
                            <span>√</span>
                            <span>≈</span>
                            <span>∞</span>
                        </div>
                        <div className="footerLegal">
                            <Link to="/">Политика конфиденциальности</Link>
                            <Link to="/">Условия использования</Link>
                        </div>
                    </div>
                </div>
            </div>
        </footer>
    )
}
export default Footer;
