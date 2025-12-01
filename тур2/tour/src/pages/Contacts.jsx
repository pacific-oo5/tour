import React, { useState } from "react";
import "../CSS/Contacts.css";

export default function Contacts() {
  const [form, setForm] = useState({ name: "", email: "", message: "" });

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Спасибо, ${form.name}! Ваше сообщение отправлено.`);
    setForm({ name: "", email: "", message: "" });
  };

  return (
    <div className="contacts-page">
      <div className="contacts-header">
        <h1>Свяжитесь с нами</h1>
        <p>Мы всегда рады вашим вопросам и предложениям 🌴</p>
      </div>

      <div className="contacts-container">
        <div className="contacts-info">
          <h2>Контактная информация</h2>
          <p><b>Адрес:</b> г. Бишкек, ул. Туристическая, 23</p>
          <p><b>Email:</b> info@skytravel.kg</p>
          <p><b>Телефон:</b> +996 555 123 456</p>

          <div className="socials">
            <a href="#"><img src="https://img.icons8.com/ios-filled/50/ffffff/facebook-new.png" alt="Facebook"/></a>
            <a href="#"><img src="https://img.icons8.com/ios-filled/50/ffffff/instagram-new.png" alt="Instagram"/></a>
            <a href="#"><img src="https://img.icons8.com/ios-filled/50/ffffff/twitter.png" alt="Twitter"/></a>
          </div>
        </div>

        <form className="contacts-form" onSubmit={handleSubmit}>
          <h2>Отправить сообщение</h2>
          <input
            type="text"
            placeholder="Ваше имя"
            value={form.name}
            onChange={(e) => setForm({...form, name: e.target.value})}
            required
          />
          <input
            type="email"
            placeholder="Email"
            value={form.email}
            onChange={(e) => setForm({...form, email: e.target.value})}
            required
          />
          <textarea
            placeholder="Сообщение"
            value={form.message}
            onChange={(e) => setForm({...form, message: e.target.value})}
            required
          />
          <button type="submit">Отправить</button>
        </form>
      </div>
    </div>
  );
}
