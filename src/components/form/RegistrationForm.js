import "./RegistrationForm.css";

function RegistrationForm({ isRegistrationFormOpen, onClose }) {
  if (!isRegistrationFormOpen) {
    return null;
  }

  const handleSubmit = (event) => {
    event.preventDefault();
  };

  return (
    <div className="registrationOverlay" onClick={onClose}>
      <form
        className="registrationForm"
        onClick={(event) => event.stopPropagation()}
        onSubmit={handleSubmit}
      >
        <button className="registrationClose" type="button" onClick={onClose}>
          Закрыть
        </button>
        <h2>Регистрация</h2>
        <div className="form-group">
          <label htmlFor="email">email</label>
          <input type="email" id="email" name="email" />
          <label htmlFor="password">Введите пароль</label>
          <input type="password" id="password" name="password" />
          <label htmlFor="confirmPassword">Подтвердите пароль</label>
          <input type="password" id="confirmPassword" name="confirmPassword" />
          <button type="submit">Зарегистрироваться</button>
        </div>
      </form>
    </div>
  );
}

export default RegistrationForm;
