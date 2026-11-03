import Logo from "../logoSite/Logo"; /* импортируем логотип чтобы распорложить его на форме входа */
import "./loginForm.css";

function LoginForm({onClose, isLoginFormOpen, onForm}) {
    if (!isLoginFormOpen) {
        return null;
    }

    const handleSubmit = (event) => {
        event.preventDefault();
    }
    return (
        <div className='loginOverlay'> {/* контейнер для формы входа */}
            <form
                className='loginForm'
                onClick={(event) => event.stopPropagation()} /* клик по форме не закрывает форму */
                onSubmit={handleSubmit} /* отправка формы (т.е. вызов функции handleSubmit), отмена перезагрузки странцы */
            >
                {/* кнопка закрытия формы */}
                <button className="registrationClose" type="button" onClick={onClose}>
                    Закрыть
                </button>
                <div className="logoEntrance">
                <Logo /> {/* логотип на форме входа */}
                <h2>Войдите в свой аккаунт</h2> {/* заголовок на форме входа */}
                </div>
                <div className="form-groupLogin">
                    <label htmlFor="email">email</label>
                    <input type="email" id="email" name="email" />
                    <label htmlFor="password">Введите пароль</label>
                    <input type="password" id="password" name="password" />
                    <button className="loginButton" type="submit">Войти</button>
                </div>
            </form>
        </div>
    )
}
export default LoginForm;