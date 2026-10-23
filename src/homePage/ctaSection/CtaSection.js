import Icons from "../../components/icons/Icons";
import { Link } from "react-router-dom";
import "./CtaSection.css"


function CtaSection() {
    return (
        <div className="wrap">
            <div className="wrapper">
                <div className="CtaCard">
                    <div className="initialConditions">
                        <Icons name="sparkles" /> {/* подключение иконки из компонента Icons */}
                        <h4>1 занятие бесплатно.</h4>
                    </div>
                    <h1>Начните решать уже сегодня</h1>
                    <p>Зарегистрируйтесь и получите первую серию задач с пошаговыми разборами. Прогресс сохраняется автоматически.</p>
                    <div className="CtaForm">
                        <Icons name="mail" /> {/* поключим иконку чтобы располоижить ее в поле ввода */}
                        <input type="email" placeholder="Введите ваш Email" />
                        <button>
                            Создать аккаунт
                            <Icons name="arrow_right" alt="" />
                        </button>
                    </div>
                    <a>Уже есть аккаунт? Войти</a>
                    <div className="CtaTrust">
                        <Icons name="check_mark" />
                        <p>Без привязки карты</p>
                        <Icons name="check_mark" />
                        <p>Отмена в один клик</p>
                        <Icons name="check_mark" />
                        <p>Доступ с телефона и ноутбука</p>
                    </div>
                </div>
            </div>
        </div>
    )
}
export default CtaSection
