import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import toursData from "../tours.json";
import "../CSS/Tours.css";

export default function Tours() {
  const [tours, setTours] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [searchText, setSearchText] = useState("");
  const [filterType, setFilterType] = useState("");
  const navigate = useNavigate();

  const toursPerPage = 9; // 9 туров на странице

  useEffect(() => {
    setTours(toursData);
  }, []);

  // Фильтруем туры по поиску и типу
  const filteredTours = tours.filter((tour) => {
    const matchesSearch = tour.title.toLowerCase().includes(searchText.toLowerCase());
    const matchesType = filterType ? tour.type.toLowerCase() === filterType.toLowerCase() : true;
    return matchesSearch && matchesType;
  });

  // расчёт пагинации
  const lastIndex = currentPage * toursPerPage;
  const firstIndex = lastIndex - toursPerPage;
  const currentTours = filteredTours.slice(firstIndex, lastIndex);
  const totalPages = Math.ceil(filteredTours.length / toursPerPage);

  const goToDetails = (id) => {
    navigate(`/details/${id}`);
  };

  // Получаем уникальные типы туров для фильтра
  const tourTypes = [...new Set(tours.map(t => t.type).filter(Boolean))];

  return (
    <div className="tours-page">
      <h2>Популярные туры</h2>

      <div className="search-filter">
        <input
          type="text"
          placeholder="Поиск по названию..."
          value={searchText}
          onChange={(e) => { setSearchText(e.target.value); setCurrentPage(1); }}
        />

        <select
          value={filterType}
          onChange={(e) => { setFilterType(e.target.value); setCurrentPage(1); }}
        >
          <option value="">Все типы</option>
          {tourTypes.map((type, idx) => (
            <option key={idx} value={type}>{type}</option>
          ))}
        </select>
      </div>

      <div className="tour-grid">
        {currentTours.map((tour) => (
          <div
            className="tour-card"
            key={tour.id}
            onClick={() => goToDetails(tour.id)}
            style={{ cursor: "pointer" }}
          >
            <img src={tour.image} alt={tour.title} />
            <h3>{tour.title}</h3>
            <p>{tour.description}</p>
            <div className="tour-price">{tour.price}$</div>
          </div>
        ))}
      </div>

      <div className="pagination">
        {[...Array(totalPages)].map((_, idx) => (
          <button
            key={idx}
            className={currentPage === idx + 1 ? "active" : ""}
            onClick={() => setCurrentPage(idx + 1)}
          >
            {idx + 1}
          </button>
        ))}
      </div>
    </div>
  );
}
