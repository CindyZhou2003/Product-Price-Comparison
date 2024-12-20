// src/App.js
import Login from './components/Login';
import Home from './components/Home';
import {BrowserRouter as Router, Routes, Route, Navigate} from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import Register from "./components/Register";
import ForgotPassword from "./components/ForgotPassword";
import Favorites from "./components/Pages/Favorites";
import Settings from "./components/Pages/Settings";
import PriceHistory from "./components/Pages/PriceHistory";
import ProductComparison from "./components/Pages/ProductComparison";


function App() {
    // 状态管理，用来跟踪用户是否已登录
  // Initialize authentication state using localStorage
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    // Retrieve the initial value from localStorage (if present)
    return localStorage.getItem("isAuthenticated") === "true";
  });

  // Update localStorage whenever isAuthenticated state changes
  useEffect(() => {
    localStorage.setItem("isAuthenticated", isAuthenticated);
  }, [isAuthenticated]);

  return (
    <Router basename={process.env.PUBLIC_URL}>
      <Routes>
        {/* If not authenticated, redirect to login page */}
        <Route path="/home" element={isAuthenticated ?
            <Home setIsAuthenticated={setIsAuthenticated} /> : <Navigate to="/login" />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot_password" element={<ForgotPassword />} />
        {/* Login page with state update */}
        <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
        {/* Default route */}
        <Route path="/" element={isAuthenticated ? <Navigate to="/home" /> : <Navigate to="/login" />} />


        {/* Home with nested routes */}
        <Route path="/home" element={<Home setIsAuthenticated={setIsAuthenticated} />}>
          <Route path="product-comparison" element={<ProductComparison />} />
          <Route path="price-history" element={<PriceHistory />} />
          <Route path="favorites" element={<Favorites />} />
          <Route path="settings" element={<Settings />} />
        </Route>
        {/*<Route path="/" element={<div>Hello World</div>} />*/}
      </Routes>
    </Router>
  );
}

export default App;