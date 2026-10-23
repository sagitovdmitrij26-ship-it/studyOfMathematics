import "./Icons.css"
 /* Создание объекта с иконками, где ключом будет имя иконки, а
 значением будет путь  к иконке */
 const icons = {
    mail: "/iconsSite/mail.png",
    sparkles: "/sparkles.png",
    check_mark: "/iconsSite/check_mark.png",
    arrow_right: "/iconsSite/right.png",
    logo: "/image/sigma.svg",
    telegram: "/iconsSite/telegram.png",
    max: "/iconsSite/max.jpg",
 }

 /* Передаем в аргумент функции деструктуризацией имя иконки, alt, className (СSS класс), 
 ...props (пропсы для иконки (width, height, onClick и т.д.)) */
function Icons({ name, alt = "", className = "", ...props }) {
    const src = icons[name]; /* для получения пути к иконке из объекта icons воспользуемся ключом
    name, который передаем в аргумент функции */
    if (!src) return null; /* если иконка не найдена, то возвращаем null */
    return (
        /* выводим img и в атрибутах его пишем класс, путь, alt (альтернативный текст) и пропсы */
        <img
        /* если передан className, то добавляем его к классу icon, иначе просто icon */
            className={className ? `icon ${className}` : "icon"}
            src={src} /* путь к иконке */
            alt={alt} /* альтернативный текст */
            {...props} /* пропсы для иконки (width, height, onClick и т.д.) */
        />
    )
}
export default Icons