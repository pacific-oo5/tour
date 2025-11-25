import React, { useEffect, useState } from "react";
import toursSeed from "../tours.json";
import bookingsSeed from "../booking.json";
import "../CSS/AdminPanel.css";

export default function AdminPanel() {
  const [tours, setTours] = useState([]);
  const [bookings, setBookings] = useState([]);
  const [editingTour, setEditingTour] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ title: "", description: "", price: 0, type: "", image: "" });
  const [filterText, setFilterText] = useState("");
  const [tab, setTab] = useState("tours");

  const currentUser = JSON.parse(localStorage.getItem("currentUser"));
  const isAdmin = currentUser?.email === "admin@gmail.com" && currentUser?.password === "admin";

  // Инициализация туров и бронирований
  useEffect(() => {
    // Туры
    const storedTours = JSON.parse(localStorage.getItem("tours"));
    if (!storedTours || storedTours.length === 0) {
      localStorage.setItem("tours", JSON.stringify(toursSeed));
      setTours(toursSeed);
    } else {
      setTours(storedTours);
    }

    // Бронирования
    localStorage.setItem("bookings", JSON.stringify(bookingsSeed.bookings));
    setBookings(bookingsSeed.bookings);
  }, []);

  // Сохраняем туры при изменении
  useEffect(() => {
    localStorage.setItem("tours", JSON.stringify(tours));
  }, [tours]);

  // Добавление тура
  const handleAddClick = () => {
    setEditingTour(null);
    setForm({ title: "", description: "", price: 0, type: "", image: "" });
    setShowForm(true);
  };

  // Редактирование тура
  const handleEditClick = (tour) => {
    setEditingTour(tour.id);
    setForm({
      title: tour.title || "",
      description: tour.description || "",
      price: tour.price || 0,
      type: tour.type || "",
      image: tour.image || ""
    });
    setShowForm(true);
  };

  const handleDelete = (id) => {
    if (!window.confirm("Удалить тур?")) return;
    setTours(prev => prev.filter(t => t.id !== id));
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    if (editingTour) {
      setTours(prev => prev.map(t => t.id === editingTour ? { ...form, id: editingTour } : t));
      alert("Тур обновлён!");
    } else {
      setTours(prev => [{ ...form, id: Date.now() }, ...prev]);
      alert("Тур добавлен!");
    }
    setShowForm(false);
  };

  const visibleTours = tours.filter(t =>
    t.title.toLowerCase().includes(filterText.toLowerCase()) ||
    (t.type || "").toLowerCase().includes(filterText.toLowerCase())
  );

  if (!isAdmin) return <div className="not-admin">Войдите как <b>admin@gmail.com / admin</b> для доступа</div>;

  return (
    <div className="admin-page">
      <h1 className="admin-title">SkyTravel — Админ-панель</h1>

      <div className="admin-tabs">
        {["tours","bookings","reports"].map(t => (
          <button
            key={t}
            className={tab===t?"active-tab":""}
            onClick={()=>setTab(t)}
          >
            {t==="tours"?"Туры":t==="bookings"?"Бронирования":"Отчётность"}
          </button>
        ))}
      </div>

      {tab==="tours" && (
        <div className="tab-content">
          <div className="tours-header">
            <button className="btn-add" onClick={handleAddClick}>Добавить тур</button>
            <input
              className="search-input"
              placeholder="Поиск..."
              value={filterText}
              onChange={e=>setFilterText(e.target.value)}
            />
          </div>

          <div className="tours-list">
            {visibleTours.map(t => (
              <div key={t.id} className="tour-card">
                {t.image && <img src={t.image} alt={t.title} className="tour-image"/>}
                <h3>{t.title}</h3>
                <p>{t.description}</p>
                <p><b>Цена:</b> {t.price}$ | <b>Тип:</b> {t.type}</p>
                <div className="tour-actions">
                  <button onClick={()=>handleEditClick(t)}>Редактировать</button>
                  <button onClick={()=>handleDelete(t.id)} className="btn-delete">Удалить</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Модальное окно формы */}
      {showForm && (
        <div className="modal-overlay">
          <div className="modal-content">
            <form onSubmit={handleFormSubmit}>
              <h3>{editingTour ? "Редактировать тур" : "Добавить тур"}</h3>
              <input
                placeholder="Название"
                value={form.title}
                onChange={e=>setForm({...form, title:e.target.value || ""})}
              />
              <textarea
                placeholder="Описание"
                value={form.description}
                onChange={e=>setForm({...form, description:e.target.value || ""})}
              />
              <input
                placeholder="Цена"
                type="number"
                value={form.price}
                onChange={e=>setForm({...form, price: +e.target.value || 0})}
              />
              <input
                placeholder="Тип"
                value={form.type}
                onChange={e=>setForm({...form, type:e.target.value || ""})}
              />
              <input
                placeholder="Ссылка на изображение"
                value={form.image}
                onChange={e=>setForm({...form, image:e.target.value || ""})}
              />
              <div className="form-buttons">
                <button type="submit" className="btn-save">Сохранить</button>
                <button type="button" onClick={()=>setShowForm(false)} className="btn-cancel">Отмена</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {tab==="bookings" && (
        <div className="tab-content bookings-tab">
          {bookings.length===0 ? <p>Бронирований нет</p> :
            bookings.map(b => (
              <div key={b.id} className="booking-card">
                <p><b>Тур:</b> {b.tourTitle} | <b>Имя:</b> {b.userName} | <b>Email:</b> {b.email}</p>
                <p><b>Цена:</b> {b.price}$ | <b>Дата:</b> {new Date(b.date).toLocaleString()} | <b>Статус оплаты:</b> {b.paymentStatus}</p>
              </div>
            ))
          }
        </div>
      )}

      {tab === "reports" && (
        <div className="tab-content reports-tab">
          <h2>📊 Общая отчётность SkyTravel</h2>

          <div className="report-cards">
            <div className="report-card">
              <h3>Туры</h3>
              <p>Всего туров: <b>{tours.length}</b></p>
            </div>

            <div className="report-card">
              <h3>Бронирования</h3>
              <p>Всего бронирований: <b>{bookings.length}</b></p>
              <p>Оплачено: <b style={{color: "green"}}>{bookings.filter(b => b.paymentStatus === "paid").length}</b></p>
              <p>В ожидании: <b style={{color: "orange"}}>{bookings.filter(b => b.paymentStatus === "pending").length}</b></p>
            </div>

            <div className="report-card">
              <h3>💰 Финансы</h3>
              <p>Общая выручка: <b>{bookings.filter(b => b.paymentStatus === "paid").reduce((sum, b) => sum + b.price, 0)}$</b></p>
              <p>Средняя стоимость тура: <b>
                {bookings.length > 0
                  ? Math.round(bookings.reduce((sum, b) => sum + b.price, 0) / bookings.length)
                  : 0
                }$
              </b></p>
            </div>

            <div className="report-card">
              <h3>📅 Последние бронирования</h3>
              {bookings.slice(0, 7).map(b => (
                <p key={b.id}>
                  {b.tourTitle} — {b.userName} — {b.price}$ — {b.paymentStatus === "paid" ? <span style={{color:"green"}}>Оплачено</span> : <span style={{color:"orange"}}>В ожидании</span>}
                </p>
              ))}
              {bookings.length === 0 && <p>Нет бронирований</p>}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
