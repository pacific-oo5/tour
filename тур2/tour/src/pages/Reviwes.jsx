import React, { useState } from "react";
import { motion } from "framer-motion";
import "../CSS/Reviews.css";

export default function Reviews() {
  const [reviews, setReviews] = useState([
    {
      id: 1,
      name: "Алина Петрова",
      avatar: "https://randomuser.me/api/portraits/women/44.jpg",
      text: "Поездка прошла идеально! Организация на высшем уровне — лучшие впечатления!",
      rating: 5,
      date: "2025-01-10",
    },
    {
      id: 2,
      name: "Иван Воробьёв",
      avatar: "https://randomuser.me/api/portraits/men/11.jpg",
      text: "Очень понравился сервис и внимательность сотрудников. Спасибо большое!",
      rating: 4,
      date: "2025-02-01",
    },
    {
      id: 3,
      name: "Саида Мухтарова",
      avatar: "https://randomuser.me/api/portraits/women/65.jpg",
      text: "Невероятно! Фото не передаёт того, что я увидела на самом деле!",
      rating: 5,
      date: "2025-03-05",
    },
  ]);

  const [newReview, setNewReview] = useState({ name: "", text: "", rating: 5 });

  const addReview = () => {
    if (!newReview.name || !newReview.text) return;

    setReviews([
      {
        id: Date.now(),
        avatar: "https://randomuser.me/api/portraits/lego/1.jpg",
        date: new Date().toISOString().split("T")[0],
        ...newReview,
      },
      ...reviews,
    ]);

    setNewReview({ name: "", text: "", rating: 5 });
  };

  return (
    <div className="reviews-page">

      <h2 className="reviews-title">Отзывы наших путешественников</h2>
      <p className="reviews-subtitle">Только реальные истории и эмоции</p>

      {/* Форма */}
      <div className="review-form">
        <input
          type="text"
          placeholder="Ваше имя"
          value={newReview.name}
          onChange={(e) => setNewReview({ ...newReview, name: e.target.value })}
        />

        <textarea
          placeholder="Ваш отзыв..."
          value={newReview.text}
          onChange={(e) => setNewReview({ ...newReview, text: e.target.value })}
        ></textarea>

        <select
          value={newReview.rating}
          onChange={(e) =>
            setNewReview({ ...newReview, rating: Number(e.target.value) })
          }
        >
          <option value="5">⭐⭐⭐⭐⭐ (5)</option>
          <option value="4">⭐⭐⭐⭐ (4)</option>
          <option value="3">⭐⭐⭐ (3)</option>
          <option value="2">⭐⭐ (2)</option>
          <option value="1">⭐ (1)</option>
        </select>

        <button onClick={addReview}>Добавить отзыв</button>
      </div>

      {/* Список отзывов */}
      <div className="reviews-grid">
        {reviews.map((rev) => (
          <motion.div
            className="review-card"
            key={rev.id}
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
          >
            <img className="review-avatar" src={rev.avatar} alt={rev.name} />
            <div className="review-content">
              <h3>{rev.name}</h3>

              <div className="stars">
                {"⭐".repeat(rev.rating)}
              </div>

              <p className="review-text">{rev.text}</p>
              <p className="review-date">
                {new Date(rev.date).toLocaleDateString()}
              </p>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
