import "./entrance.css";

/* Компонент входа в личный кабинет: принимает children и отображает их внутри */
function Entrance({ children }) {
  return (
    <div className="entrance">
      {children}
      
      {/* <input type="text" name = "login" placeholder="Введите логин" />
      <input type="password" name = "password" placeholder="Введите пароль" />
       <input type="password" name = "password" placeholder="Подтвердите пароль" />
       <button type="submit">Войти</button> */}
    </div>
    
  );
}

export default Entrance;