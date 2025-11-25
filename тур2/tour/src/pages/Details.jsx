
import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import toursData from "../tours.json";
import "../CSS/Details.css";

export default function Details() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [tour, setTour] = useState(null);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    const selectedTour = toursData.find((t) => t.id === parseInt(id));
    setTour(selectedTour);
  }, [id]);

  if (!tour) return <p>Загрузка...</p>;

  const handleBooking = () => {
    alert(`Вы забронировали тур: ${tour.title}`);
    navigate("/payment"); // переходим на страницу оплаты
  };

  const handleSave = () => {
    setSaved(!saved);
    alert(saved ? `Тур ${tour.title} удалён из сохранённых` : `Тур ${tour.title} добавлен в сохранённые`);
  };

  return (
    <div className="details-page">
      <div className="tour-detail-card">
        <img src={tour.image} alt={tour.title} />
        <div className="tour-detail-info">
          <h2>{tour.title}</h2>
          <p>{tour.description}</p>
          <p className="price">от {tour.price}$</p>
          <p>Тип тура: {tour.type}</p>

          <div className="tour-buttons">
            <button className="book-btn" onClick={handleBooking}>
              Забронировать
            </button>
            <button className="save-btn" onClick={handleSave}>
              {saved ? "Удалить из сохранённых" : "Сохранить тур"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
