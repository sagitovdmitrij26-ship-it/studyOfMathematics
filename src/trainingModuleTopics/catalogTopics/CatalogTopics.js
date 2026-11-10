import { useState } from 'react';
import Icons from '../../components/icons/Icons';
import CatalogTopicList from '../catalogTopicList/CatalogTopicList';
import './CatalogTopics.css';

function CatalogTopics({ catalogTopicLists }) {
    /* напишем хук для выбора класса useState */
    const [activeClass, setActiveClass] = useState(null) /* значение по умолчанию null без "" чтобы отработал код в CatalogTopicList (запасной текст) */
    /* НАпишем хук для выбора уровня сложности */
    const [ isDifficultyLevel, setIsDifficultyLevel ] = useState(null)
    return (
        <div className="wrap"> {/* внутренняя обертка */}
            <div className="wrapper"> {/* внутренняя обертка 2*/}
                <div className='catalogMain'> {/* Общий блок для раздела с темами */}
                    <div className='catalogMain__title'> {/* Заголовок раздела */}
                        <h1>Каталог тем</h1>
                        <p>12 разделов, 680 задач и 240 разборов. Выберите
                            тему — тренажёр подстроит сложность под ваш уровень.</p>
                        <div className='catalogMain_toolbar'> {/* Блок для панели инструментов */}
                            <div className='catalogMain_search'>
                                <Icons name="search" alt="" />
                                <input type="text" placeholder='Поиск темы или правила' />
                            </div>
                            <p>Выберите класс:</p>
                            <div className='classSelection'> {/* Блок для выбора класса */}
                                <button type='button' onClick={() => setActiveClass("5–6 класс")}>5–6 класс</button>
                                <button type='button' onClick ={() => setActiveClass("7 класс")}>7 класс</button>
                                <button type='button' onClick ={() => setActiveClass("8 класс")}>8 класс</button>
                                <button type='button' onClick ={() => setActiveClass("9 класс")}>9 класс</button>
                            </div>
                        </div>
                        <div className='difficuktyLevel'> {/* блок с выбором уровня сложности */}
                            <p>Выберите уровень сложности:</p>
                            <button onClick ={ () => setIsDifficultyLevel("Базовый") }>Базовый</button> {/* укажем что при нажатии на кнопку будет срабатывать функция setIsDifficultyLevel */}
                            <button onClick ={ () => setIsDifficultyLevel("Средний") }>Средний</button> {/* укажем что при нажатии на кнопку будет срабатывать функция setIsDifficultyLevel */}
                            <button onClick ={ () => setIsDifficultyLevel("Высокий") }>Высокий</button> {/* укажем что при нажатии на кнопку будет срабатывать функция setIsDifficultyLevel */}
                            
                        </div>
                        <CatalogTopicList
                            catalogTopicLists={catalogTopicLists}
                            activeClass={activeClass}
                            isDifficultyLevel={isDifficultyLevel}
                        />
                    </div>
                </div>
            </div>
        </div>
    )
}
export default CatalogTopics;