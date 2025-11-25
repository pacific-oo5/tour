// server.js
const express = require("express");
const fs = require("fs");
const cors = require("cors");
const app = express();
const PORT = 5001;

app.use(cors());
app.use(express.json());

const bookingsFile = "./bookings.json";

// Создание новой брони
app.post("/bookings", (req, res) => {
  const booking = req.body;

  let bookings = [];
  if (fs.existsSync(bookingsFile)) {
    bookings = JSON.parse(fs.readFileSync(bookingsFile, "utf-8"));
  }

  booking.id = Date.now();
  bookings.push(booking);

  fs.writeFileSync(bookingsFile, JSON.stringify(bookings, null, 2));
  res.status(201).json({ message: "Бронь сохранена", booking });
});

// Получение всех броней
app.get("/bookings", (req, res) => {
  let bookings = [];
  if (fs.existsSync(bookingsFile)) {
    bookings = JSON.parse(fs.readFileSync(bookingsFile, "utf-8"));
  }
  res.json(bookings);
});

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
