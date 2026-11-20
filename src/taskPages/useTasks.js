/* импортируем хуки и supabase для работы с базой данных */
import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { supabase } from "../supabaseClient";

function useTasks(subject) {
    /* перенесем сюда то, без чего не работает useEffect */
    /* useSearchParams возвращает объект с методами get/set. Нам нужен только get — читать, не менять */
    const [searchParams] = useSearchParams();
    /* get("class") берёт значение параметра class. Имя должно совпасть с тем, что в search у navigate */
    /* Если открыли /Arithmetic без хвоста, get вернёт null — тогда фильтр по классу/уровню ниже не применится */
    const selectedClass = searchParams.get("class");
    const selectedLevel = searchParams.get("level");
    /* tasks — массив задач, который увидит JSX. Сначала он пустой, страница рисуется без списка */
    /* setTasks — функция, которой мы потом положим ответ из базы; после этого React перерисует компонент */
    const [tasks, setTasks] = useState([]);
/* =============================================================== */
    useEffect(() => {
        /* async — помечает функцию: внутри можно ждать сервер через await, не блокируя весь сайт */
        const fetchTasks = async () => {
            /* supabase берётся из supabaseClient.js. Если нет URL/ключа в .env.local, там null */
            /* return — выходим из функции, запрос не отправляем, иначе будет ошибка */
            if (!supabase) {
                return;
            }

            /* await — ждём ответ. Без него data ещё не будет готова */
            /* { data, error } — из ответа сразу достаём два поля: массив строк и ошибку */
            /* query собираем по шагам: сначала предмет, потом при необходимости класс и уровень */
            /* let, не const — ниже к цепочке дописываем .eq, переменную нужно перезаписать */
            let query = supabase
                .from("arithmetic_tasks") /* новая таблица с теми же колонками, что у tasks */
                .select("*") /* какие колонки взять; * = все колонки строки */
                .eq("subject", subject); /* фильтр: arithmetic или algebra — то, что передали в хук */

            /* .eq(колонка, значение) = «оставь строки, где колонка точно равна значению» */
            /* Имена колонок class_name и level — как в Table Editor, не как в каталоге (там пропсы activeClass / isDifficultyLevel) */
            /* Текст значения должен совпасть с кнопкой: «5–6 класс», «Базовый». «базовый» или «5-6» не подойдут */
            if (selectedClass) {
                query = query.eq("class_name", selectedClass);
            }
            if (selectedLevel) {
                query = query.eq("level", selectedLevel);
            }

            /* order в конце цепочки: сортировка уже отфильтрованного набора по id */
            const { data, error } = await query.order("id").limit(5);

            /* error будет, если нет таблицы, нет колонки или RLS не даёт SELECT */
            /* return — не вызываем setTasks, чтобы не затереть состояние битым ответом */
            if (error) {
                console.log(error); /* смотрите сообщение в консоли браузера (F12) */
                return;
            }

            /* data — уже массив задач с сервера */
            /* ?? [] — если data вдруг null, кладём пустой массив, чтобы потом можно было писать tasks.map */
            /* setTasks запоминает массив и заставляет React перерисовать страницу заново уже с задачами */
            setTasks(data ?? []);
        };

        /* Объявить fetchTasks мало: React сам её не запустит. Вызов отправляет запрос */
        fetchTasks();
        /* Второй аргумент useEffect — зависимости. Раньше был []: загрузить один раз при входе на страницу */
        /* Теперь в массиве selectedClass и selectedLevel: если в ссылке сменились класс или уровень, эффект запустится снова */
        /* Сами setTasks сюда не ставим — иначе после каждого ответа базы эффект крутился бы бесконечно */
    }, [selectedClass, selectedLevel, subject]);

    return { tasks, selectedClass, selectedLevel };
}

export default useTasks;