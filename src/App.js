import { useRef, useState } from "react";
import Header from "./components/header/Header";
import Hero from "./components/hero/Hero";
import Notification from "./components/notification/Notification";
import notificationVariants from "./components/notification/notificationVariants";
/* Импортируем блок с темами */
import TopicsSection from "./components/topicsSection/TopicsSection";
/* Импортируем блок с преимуществами */
import Advantages from "./components/advantages/Advantages";
/* Импортируем данные о темах из JSON-файла */
import topics from "./topic.json";

import "./App.css";

function App() {
  const [activeNotification, setActiveNotification] = useState(null);
  const hideTimerRef = useRef(null);

  /* Показывает уведомление по индексу из массива notificationVariants */
  const showNotification = (index) => {
    setActiveNotification(notificationVariants[index]);

    /* Сбрасываем предыдущий таймер автозакрытия, если клик был повторным */
    if (hideTimerRef.current) {
      clearTimeout(hideTimerRef.current);
    }

    /* Автоматически скрываем уведомление через 6 секунды */
    hideTimerRef.current = setTimeout(() => {
      setActiveNotification(null);
    }, 6000);
  };

  /* При клике на "Войти" показываем уведомление о необходимости регистрации */
  const handleLoginClick = () => {
    showNotification(2);
  };

  return (
    <div className="App">
      {/* При клике на "Войти" показываем уведомление о необходимости регистрации */}
      <Header onForm={handleLoginClick} />
      {/* При клике на «Начать бесплатно» показываем первое уведомление (success) */}
      <Hero onStart={() => showNotification(2)} />
      {activeNotification && <Notification variant={activeNotification} />}    
      <TopicsSection topics={topics.topics} />  {/* Блок с темами подключаем */}
      <Advantages advantages={topics.advantages} /> {/*Подключаем блок с преимуществами  */}
    </div>
  );
}

export default App;
