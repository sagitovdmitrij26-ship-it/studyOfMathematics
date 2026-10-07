import "./Notification.css";

/* Компонент уведомления: получает объект варианта из notificationVariants
   и рендерит его готовую разметку поверх страницы */
function Notification({ variant }) {
  if (!variant) return null;

  return <div className="notificationContainer">{variant.markup}</div>;
}

export default Notification;
