import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Tours from "./pages/Tours";
import Register from "./pages/Register";
import Login from "./pages/Login";
import Payment from "./pages/Payment";
import Details from "./pages/Details";
import AdminPanel from "./pages/AdminPanel";
import Reviews from "./pages/Reviwes";
import Contacts from "./pages/Contacts";

function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/tours" element={<Tours />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/payment" element={<Payment />} />
        <Route path="/details/:id" element={<Details />} />
        <Route path="/admin" element={<AdminPanel />} />
        <Route path="/reviews" element={<Reviews />} />
         <Route path="/contact" element={<Contacts />} />
      </Routes>
    </>
  );
}

export default App;
