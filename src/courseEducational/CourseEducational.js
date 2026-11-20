import "./CourseEducational.css";

function CourseEducational({ badgeText }) {
    return (
        <div className="wrap">
            <div className="wrapper">
                <section className="course-hero">
                    <div className="badge">
                        <span></span>
                        <h4>{badgeText}</h4>
                    </div>
                    <div className="title">
                        <h1>Курс математики<br />для 5–9 класса</h1>
                        <p>
                            4 раздела, 3430 задач с подробными решениями и объяснениями
                            для уверенного освоения школьной программы.
                        </p>
                    </div>
                    <div className="course-stats">
                        <div className="course-stat">
                            <img src="/iconsCourse/stat-sections.png" alt="" />
                            4 раздела
                        </div>
                        <div className="course-stat">
                            <img src="/iconsCourse/stat-tasks.png" alt="" />
                            3430 задач
                        </div>
                        <div className="course-stat">
                            <img src="/iconsCourse/stat-levels.png" alt="" />
                            3 уровня
                        </div>
                    </div>
                    <div className="course-cta">
                        <span className="course-cta__primary">К каталогу тем →</span>
                        <span className="course-cta__secondary">Как устроен курс</span>
                    </div>
                </section>

                <section className="course-program">
                    <h2>Программа</h2>
                    <div className="program-grid">
                        <article className="program-card">
                            <h3>Арифметика</h3>
                            <p className="program-card__class">5–9 класс</p>
                            <ul>
                                <li>Делимость и НОД</li>
                                <li>Дроби и проценты</li>
                                <li>Пропорции и масштабы</li>
                            </ul>
                            <div className="program-card__levels">
                                <span className="program-card__level program-card__level--basic">Базовый</span>
                                <span className="program-card__level program-card__level--medium">Средний</span>
                                <span className="program-card__level program-card__level--high">Высокий</span>
                            </div>
                        </article>
                        <article className="program-card">
                            <h3>Алгебра</h3>
                            <p className="program-card__class">5–9 класс</p>
                            <ul>
                                <li>Выражения и тождества</li>
                                <li>Уравнения и неравенства</li>
                                <li>Системы уравнений</li>
                            </ul>
                            <div className="program-card__levels">
                                <span className="program-card__level program-card__level--basic">Базовый</span>
                                <span className="program-card__level program-card__level--medium">Средний</span>
                                <span className="program-card__level program-card__level--high">Высокий</span>
                            </div>
                        </article>
                        <article className="program-card">
                            <h3>Геометрия</h3>
                            <p className="program-card__class">5–9 класс</p>
                            <ul>
                                <li>Плоские фигуры</li>
                                <li>Треугольники и окружности</li>
                                <li>Площади и теоремы</li>
                            </ul>
                            <div className="program-card__levels">
                                <span className="program-card__level program-card__level--basic">Базовый</span>
                                <span className="program-card__level program-card__level--medium">Средний</span>
                                <span className="program-card__level program-card__level--high">Высокий</span>
                            </div>
                        </article>
                        <article className="program-card">
                            <h3>Функции</h3>
                            <p className="program-card__class">с 7 класса</p>
                            <ul>
                                <li>Линейные функции</li>
                                <li>Квадратичные функции</li>
                                <li>Графики и свойства</li>
                            </ul>
                            <div className="program-card__levels">
                                <span className="program-card__level program-card__level--basic">Базовый</span>
                                <span className="program-card__level program-card__level--medium">Средний</span>
                                <span className="program-card__level program-card__level--high">Высокий</span>
                            </div>
                        </article>
                    </div>
                </section>

                <section className="course-flow">
                    <h2>Как проходит занятие</h2>
                    <div className="flow-row">
                        <div className="flow-step">
                            <span className="flow-step__num">01</span>
                            <h3>Класс</h3>
                            <img src="/iconsCourse/step-class.png" alt="" />
                        </div>
                        <div className="flow-line"></div>
                        <div className="flow-step">
                            <span className="flow-step__num">02</span>
                            <h3>Уровень</h3>
                            <img src="/iconsCourse/step-level.png" alt="" />
                        </div>
                        <div className="flow-line"></div>
                        <div className="flow-step">
                            <span className="flow-step__num">03</span>
                            <h3>Практика</h3>
                            <img src="/iconsCourse/step-practice.png" alt="" />
                        </div>
                        <div className="flow-line"></div>
                        <div className="flow-step">
                            <span className="flow-step__num">04</span>
                            <h3>Разбор</h3>
                            <img src="/iconsCourse/step-review.png" alt="" />
                        </div>
                    </div>
                </section>
            </div>
        </div>
    )
}

export default CourseEducational;
