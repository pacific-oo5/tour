import React, { useEffect, useState } from "react";
import "../CSS/Navbar.css";
import { useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const currentUser = JSON.parse(localStorage.getItem("currentUser"));
    if (currentUser) setUser(currentUser);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("currentUser");
    setUser(null);
    navigate("/");
  };

  return (
    <header className="navbar">
      <div className="navbar-logo" onClick={() => navigate("/")}>
        SkyTravel
      </div>

      <nav className="navbar-links">
        <button onClick={() => navigate("/")}>Главная</button>
        <button onClick={() => navigate("/tours")}>Туры</button>
        <button onClick={() => navigate("/reviews")}>Отзывы</button>
        <button onClick={() => navigate("/contact")}>Контакты</button>
      </nav>

      <div className="navbar-auth">
        {!user ? (
          <>
            <button className="auth-btn" onClick={() => navigate("/register")}>
              Регистрация
            </button>
            <button className="auth-btn login" onClick={() => navigate("/login")}>
              Вход
            </button>
          </>
        ) : (
          <>
            {user.email === "admin@gmail.com" && user.password === "admin" ? (
              <button className="auth-btn" onClick={() => navigate("/admin")}>
                Админ панель
              </button>
            ) : (
              <button className="auth-btn" onClick={() => navigate("/saved-tours")}>
                Сохранённые туры
              </button>
            )}
            <button className="auth-btn login" onClick={handleLogout}>
              Выйти
            </button>
          </>
        )}
      </div>
    </header>
  );
}
