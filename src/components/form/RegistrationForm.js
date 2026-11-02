import "./RegistrationForm.css"; /* Подключение стилей формы */
import { useState } from "react"; /* Подключим useState для выбора аватара */
import avatarImage from "../../avatarImage.json"; /* Подключим файл с аватарами */
import Logo from "../logoSite/Logo";

/* создание функционально компонента RegistrationForm, в которрый передаем пропсы
isRegistrationFormOpen - это пропс, который определяет, открыта ли форма регистрации
onClose - это функция, которая закрывает форму регистрации
*/
function RegistrationForm({ isRegistrationFormOpen, onClose, }) {
  const [selectAvatar, setSelectAvatar] = useState(null); //создание переменной и функции выбора аватара. Сначала
  // состояние null
  const [avatarList, setAvatarList] = useState(false); //создание переменной с списком аватаром и функции
  //для открытия списка аватаров
  /* условие, если форма не открыта, то не возвращаем ноль, то есть ничего */
  if (!isRegistrationFormOpen) {
    return null;
  }
  /* Напишем функцию, которая будет предотвращать отправку формы 
  при перезагрузке страницы */
  const handleSubmit = (event) => {
    event.preventDefault();
  };

  /* Зададим переменную поиска нужной аватарки методом find() */
  const foudedAvatar = avatarImage.avatars.find((avatar) => avatar.id === selectAvatar);

  /* создание функции, благодаря которой видим список аватарок */
  const avatarListClose = () => {
    setAvatarList(false);
    onClose();
  }

  return (
    <div className="registrationOverlay" onClick={avatarListClose}>
      <form
        className="registrationForm"
        onClick={(event) => event.stopPropagation()}
        onSubmit={handleSubmit}
      >
        <button className="registrationClose" type="button" onClick={avatarListClose}>
          Закрыть
        </button>
        <div className="logo">
          <Logo />
          <h2>Регистрация</h2>
        </div>
        <div className="form-group">
          <label htmlFor='name'>Введите имя</label>
          <input type="text" id="name" name="name" />
          <label htmlFor='class-number'>Введите номер класса</label>
          <input type="number" id="class-number" name="class-number" />
          <label htmlFor="email">email</label>
          <input type="email" id="email" name="email" />
          <label htmlFor="password">Введите пароль</label>
          <input type="password" id="password" name="password" />
          <label htmlFor="confirmPassword">Подтвердите пароль</label>
          <input type="password" id="confirmPassword" name="confirmPassword" />
          <label htmlFor="avatar">Выберите аватар</label>
          <div className="avatarSelect">
            <button /* кнопка для будущего всплывающего списка с картинками и подписями */
              className="avatarSelectButton" /* класс для  списка */
              type="button"
              onClick={() => setAvatarList(true)} /* функция, которая при нажатии на кнопку открывает список */
            >
              {/* тернарный оператор, для проверки выбран ли аватар. ДЛя этого используем переменную foudedAvatar которая
              методом find() находит аватар по id из json файла*/}
              {foudedAvatar ? (
                <>
                  <img src={foudedAvatar.image} alt={foudedAvatar.name} /> {/* картинка аватара из json */}
                  <span>{foudedAvatar.name}</span> {/* подпись аватара из json */}
                </>
              ) : (
                <span>Выберите аватар</span> /* подпись, если аватар не выбран */
              )}
            </button>
            {/* создадим список аватарок с текстом, который будет отображаться при наведении на кнопку */}
            {avatarList && (
              <ul className="avatarSelectList">
                {avatarImage.avatars.map((avatar) => (
                  <li key={avatar.id}>
                    <button
                      type="button"
                      className={
                        avatar.id === selectAvatar
                          ? "avatarOption avatarOption--active"
                          : "avatarOption"
                      }
                      onClick={() => {
                        setSelectAvatar(avatar.id);
                        setAvatarList(false);
                      }}
                    >
                      <img src={avatar.image} alt={avatar.name} />
                      <span>{avatar.name}</span>
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>
          <input type="hidden" name="avatar" value={selectAvatar || ""} />
          <button type="submit">Зарегистрироваться</button>
        </div>
      </form>
    </div>
  );
}

export default RegistrationForm;
