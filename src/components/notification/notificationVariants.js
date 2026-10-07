import "./Notification.css";

/* Массив объектов с вариантами уведомлений и их JSX-разметкой */
/* Пути из public/ задаются строкой с ведущим "/" — импортировать нельзя */

const notificationVariants = [
  {
    type: "success", /* Варинат успех с иконкой */
    message: "Регистрация успешно завершена", /* Текст сообщения */
    icon: "/image/good.png", /* Путь к иконке */ 
    /* Разметка уведомления об успешной регистрации */
    markup: /* разметка для уведомления об успешной регистрации */( 
      <div className="notification notification--success">
        <img
          className="notification__icon"
          src="/image/good.png"
          alt="Успешно"
        />
        <p className="notification__message">Регистрация успешно завершена</p>
      </div>
    ),
  },
  {
    type: "error", /* Варинат ошибка с иконкой */
    message: "Ошибка при регистрации", /* Текст сообщения */
    icon: "/image/error.png", /* Путь к иконке */
    /* Разметка уведомления об ошибке при регистрации */
    markup: (
      <div className="notification notification--error">
        <img
          className="notification__icon"
          src="/image/error.png"
          alt="Ошибка"
        />
        <p className="notification__message">Ошибка при регистрации</p>
      </div>
    ),
  },
  {
    type: "warning", /* Варинат предупреждение с иконкой */
    message: "Нужна регистрация", /* Текст сообщения */
    icon: "/image/attention.png", /* Путь к иконке */
    /* Разметка уведомления-предупреждения о необходимости регистрации */
    markup: (
      <div className="notification notification--warning">
        <img
          className="notification__icon"
          src="/image/attention.png"
          alt="Предупреждение"
        />
        <p className="notification__message">Нужна регистрация</p>
      </div>
    ),
  },
];

export default notificationVariants;