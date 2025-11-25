import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import toursData from "../tours.json";
import reviewsData from "../reviews.json";
import "../CSS/Home.css";

export default function Home() {
  const [tours, setTours] = useState([]);
  const [reviews, setReviews] = useState([]);
  const [currentTourPage, setCurrentTourPage] = useState(1);
  const [currentReviewPage, setCurrentReviewPage] = useState(1);

  const toursPerPage = 4;
  const reviewsPerPage = 3;

  useEffect(() => {
    setTours(toursData);
    setReviews(reviewsData);
  }, []);

  // --- ТУРЫ ---
  const lastTourIndex = currentTourPage * toursPerPage;
  const firstTourIndex = lastTourIndex - toursPerPage;
  const currentTours = tours.slice(firstTourIndex, lastTourIndex);
  const totalTourPages = Math.ceil(tours.length / toursPerPage);

  // --- ОТЗЫВЫ ---
  const lastReviewIndex = currentReviewPage * reviewsPerPage;
  const firstReviewIndex = lastReviewIndex - reviewsPerPage;
  const currentReviews = reviews.slice(firstReviewIndex, lastReviewIndex);
  const totalReviewPages = Math.ceil(reviews.length / reviewsPerPage);

  return (
    <div className="home-page">
      {/* HERO SECTION */}
      <section className="hero">
        <div className="hero-content">
          <h2>Открой мир вместе с нами</h2>
          <p>
            Мы поможем вам найти идеальный отдых — от горных приключений до
            морских путешествий.
          </p>
          <Link to="/tours">
            <button className="btn">Посмотреть туры</button>
          </Link>
        </div>
      </section>

      {/* TOURS */}
      <section className="tours" id="tours">
        <h2>Популярные туры</h2>

        <div className="tour-cards">
          {currentTours.map((tour) => (
            <Link
              to={`/details/${tour.id}`}
              className="tour"
              key={tour.id}
              style={{ textDecoration: "none", color: "inherit" }}
            >
              <img src={tour.image} alt={tour.title} />
              <div className="tour-content">
                <h3>{tour.title}</h3>
                <p>{tour.description}</p>
              </div>
            </Link>
          ))}
        </div>

        {/* PAGINATION ТУРОВ */}
        <div className="pagination">
          {Array.from({ length: totalTourPages }, (_, idx) => (
            <button
              key={idx}
              className={currentTourPage === idx + 1 ? "active" : ""}
              onClick={() => setCurrentTourPage(idx + 1)}
            >
              {idx + 1}
            </button>
          ))}
        </div>
      </section>

      {/* REVIEWS */}
      <section className="reviews" id="reviews">
        <h2>Отзывы клиентов</h2>

        <div className="review-cards">
          {currentReviews.map((review) => (
            <div className="review" key={review.id}>
              <p>«{review.text}»</p>
              <h4>— {review.name}</h4>
            </div>
          ))}
        </div>

        {/* PAGINATION ОТЗЫВОВ */}
        <div className="pagination">
          {Array.from({ length: totalReviewPages }, (_, idx) => (
            <button
              key={idx}
              className={currentReviewPage === idx + 1 ? "active" : ""}
              onClick={() => setCurrentReviewPage(idx + 1)}
            >
              {idx + 1}
            </button>
          ))}
        </div>
      </section>

      {/* FOOTER */}
      <footer className="footer">
        <p>© 2025 SkyTravel. Все права защищены.</p>
      </footer>
    </div>
  );
}
