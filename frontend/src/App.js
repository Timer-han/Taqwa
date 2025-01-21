import React from "react";
import { Routes, Route } from "react-router-dom";
import NavBar from "./components/NavBar"
import AddQuestion from "./pages/AddQuestion";
import Review from "./pages/Review"
import ReviewDetail from "./pages/ReviewDetail";

function App() {
  return (
    <>
      <NavBar />
      <p>{"this is env: " + process.env.REACT_APP_API_URL}</p>
      <main>
        <Routes>
          <Route path="/" element={<AddQuestion />} />
          <Route path="/review" element={<Review />} />
          <Route path="/review/:uuid" element={<ReviewDetail />} />
        </Routes>
      </main>
    </>
  );
}

export default App;
