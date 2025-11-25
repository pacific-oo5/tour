import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "../CSS/Payment.css";

export default function Payment() {
  const navigate = useNavigate();
  const location = useLocation();

  const { title, price, id: tourId } = location.state || {};

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [card, setCard] = useState("");
  const [expiry, setExpiry] = useState("");
  const [cvv, setCvv] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    // анимация
    const box = document.querySelector(".payment-container");
    box.style.transform = "scale(1.03)";
    box.style.transition = "0.3s";

    setTimeout(() => {
      // Создаём бронь
      const oldBookings = JSON.parse(localStorage.getItem("bookings")) || [];
      const newBooking = {
        id: Date.now(),
        tourId,
        tourTitle: title,
        price,
        userName: name,
        userEmail: email,
        phone,
        date: new Date().toISOString(),
        paymentMethod: "Card",
        cardNumber: card.replace(/\s/g, ""),
      };
      const updatedBookings = [newBooking, ...oldBookings];
      localStorage.setItem("bookings", JSON.stringify(updatedBookings));

      alert(`✅ Оплата успешно выполнена! Бронь на тур "${title}" сохранена 🌴`);
      box.style.transform = "scale(1)";

      navigate("/"); // возвращаем на главную
    }, 600);
  };

  return (
    <div className="payment-background">
      <div className="payment-container">
        <h2 className="h2">Оплата тура</h2>

        {title && <h3 style={{ textAlign: "center", marginBottom: "5px" }}>{title}</h3>}
        {price && <p style={{ textAlign: "center", marginBottom: "20px" }}>Сумма: <b>{price}$</b></p>}

        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label>Имя</label>
            <input
              type="text"
              placeholder="Иван Иванов"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>

          <div className="input-group">
            <label>Email</label>
            <input
              type="email"
              placeholder="example@mail.com"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="input-group">
            <label>Телефон</label>
            <input
              type="tel"
              placeholder="+996 555 555 555"
              required
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
            />
          </div>

          <div className="input-group">
            <label>Номер карты</label>
            <input
              type="text"
              placeholder="1234 5678 9012 3456"
              maxLength="19"
              required
              value={card}
              onChange={(e) =>
                setCard(e.target.value.replace(/[^\d\s]/g, ""))
              }
            />
          </div>

          <div className="card-row">
            <div className="input-group">
              <label>Срок действия</label>
              <input
                type="text"
                maxLength="5"
                placeholder="MM/YY"
                required
                value={expiry}
                onChange={(e) => setExpiry(e.target.value)}
              />
            </div>

            <div className="input-group">
              <label>CVV</label>
              <input
                type="password"
                maxLength="3"
                placeholder="***"
                required
                value={cvv}
                onChange={(e) => setCvv(e.target.value.replace(/\D/g, ""))}
              />
            </div>
          </div>

          <button type="submit" className="button">Оплатить</button>
          <p className="secure">Безопасная защита платежа</p>
        </form>
      </div>
    </div>
  );
}
