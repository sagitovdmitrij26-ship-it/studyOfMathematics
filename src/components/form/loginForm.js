import { useState } from "react";
import Logo from "../logoSite/Logo"; /* импортируем логотип чтобы распорложить его на форме входа */
import "./loginForm.css";
import { supabase } from "../../supabaseClient";

function LoginForm({onClose, isLoginFormOpen, onForm}) {
    const [error, setError] = useState("");

    if (!isLoginFormOpen) {
        return null;
    }

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError("");
        const form = event.currentTarget;
        const email = form.email.value.trim();
        const password = form.password.value;

        if (!supabase) {
            setError("Нет ключей Supabase. Добавьте .env.local и перезапустите npm start");
            return;
        }

        const { error: signInError } = await supabase.auth.signInWithPassword({
            email,
            password,
        });

        if (signInError) {
            setError(signInError.message);
            return;
        }

        onClose();
    };
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
                    {error ? <p className="form-error">{error}</p> : null}
                    <button className="loginButton" type="submit">Войти</button>
                </div>
            </form>
        </div>
    )
}
export default LoginForm;