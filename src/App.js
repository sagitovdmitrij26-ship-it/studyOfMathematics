import { Routes, Route } from "react-router-dom";
import { useRef, useState } from "react";
import Header from "./components/header/Header";
import Hero from "./homePage/hero/Hero";
import Notification from "./components/notification/Notification";
import notificationVariants from "./components/notification/notificationVariants";
/* Импортируем блок с темами */
import TopicsSection from "./homePage/topicsSection/TopicsSection";
/* Импортируем блок с преимуществами */
import Advantages from "./homePage/advantages/Advantages";
/* Импортируем блок с путем обучения */
import LeaningPath from "./homePage/learningPath/LeaningPath";
/* Импортируем блок с отзывами */
import ReviewsSection from "./homePage/reviewsSection/ReviewsSection";
/* Импортируем данные о темах из JSON-файла */
import CtaSection from './homePage/ctaSection/CtaSection';
/* Импортируем компонент Footer */
import Footer from "./components/footer/Footer";
/* Импортируем компонент RegistrationForm */
import RegistrationForm from "./components/form/RegistrationForm";
/* Импортируем компонент LoginForm */
import LoginForm from "./components/form/loginForm";
/* Импортируем компонент Arithmetic */
import Arithmetic from "./taskPages/arithmetic/Arithmetic";
/* Импортируем компонент Algebra */
import Algebra from "./taskPages/algebra/Algebra";
/* Импортируем компонент Geometry */
import Geometry from "./taskPages/geometry/Geometry";
/* Импортируем компонент Functions */
import Functions from "./taskPages/functions/Functions";
import topics from "./topic.json";
import reviews from "./review.json";
/* импорт компонента с каталогом тем */
import CatalogTopics from "./trainingModuleTopics/catalogTopics/CatalogTopics";
/* импорт компонента с описанием курса */
import CourseEducational from "./courseEducational/CourseEducational";

import "./App.css";


function App() {
  const [activeNotification, setActiveNotification] = useState(null);
  const hideTimerRef = useRef(null);
  const [isRegistrationFormOpen, setIsRegistrationFormOpen] = useState(false);
  const [isLoginFormOpen, setIsLoginFormOpen] = useState(false); // состояние для формы входа зарегестрированного пользователя

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
      {/* ===================================отрисовка компонента шгапки======================================================================= */}
      <Header
        onForm={() => setIsLoginFormOpen(true)}
        onSignUp={() => setIsRegistrationFormOpen(true)}
      />
      <RegistrationForm
        isRegistrationFormOpen={isRegistrationFormOpen}
        onClose={() => setIsRegistrationFormOpen(false)}
      />
      <LoginForm
        isLoginFormOpen={isLoginFormOpen}
        onClose={() => setIsLoginFormOpen(false)}
      />
      {/* ==================================================================================================================================== */}
      {/* ================================= */}
      <Routes> {/* оборачиваем все, кроме шапки и подвала, чтобы они всегда были на странице */}
        <Route
          path="/"
          element={
            <>
              {/* При клике на «Начать бесплатно» показываем первое уведомление (success) */}
              <Hero onStart={() => showNotification(2)} badgeText="Онлайн-тренажёр для 5-9 классов" />
              {activeNotification && <Notification variant={activeNotification} />}
              <TopicsSection topics={topics.topics} />  {/* Блок с темами подключаем */}
              <Advantages advantages={topics.advantages} /> {/*Подключаем блок с преимуществами  */}
              <LeaningPath paths={topics.paths} /> {/* Подключаем блок с путем обучения */}
              <ReviewsSection reviews={reviews.reviews} />
              <CtaSection />
            </>
          }
        />
        {/* ===================================отрисовка компонента описания курса======================================================================= */}
        <Route
          path="/CourseEducational"
          element={
            <>
              <CourseEducational badgeText="Онлайн-тренажёр для 5–9 классов" />
            </>
          }
        />
        {/* ===================================отрисовка компонента каталога тем======================================================================= */}
        <Route
          path="/catalogTopics"
          element={
            <>
              <CatalogTopics catalogTopicLists={topics.catalogTopicLists} />
            </>
          }
        />
        <Route
          path="/Arithmetic"
          element={
            <>
              < Arithmetic />
            </>
          }
        />
        <Route
          path="/Algebra"
          element={
            <>
              < Algebra />
            </>
          }
        />
        <Route
          path="/Geometry"
          element={
            <>
              < Geometry />
            </>
          }
        />
        <Route
          path="/Functions"
          element={
            <>
              < Functions />
            </>
          }
        />
        {/* ===================================================================================================================================== */}

      </Routes>
      <Footer />
    </div>
  );
}

export default App;
