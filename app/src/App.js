// App.js
import './css/App.css';
import Login from './components/Login';
import Home from './components/Home';
import {BrowserRouter as Router, Routes, Route, Navigate} from 'react-router-dom';
import React, { useState } from 'react';
import Register from "./components/Register";


function App() {
    // 状态管理，用来跟踪用户是否已登录
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  return (
    <Router>
      <Routes>
        {/* If not authenticated, redirect to login page */}
        <Route path="/home" element={isAuthenticated ? <Home setIsAuthenticated={setIsAuthenticated} /> : <Navigate to="/login" />} />
        <Route path="/register" element={<Register />} />
        {/* Login page with state update */}
        <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
        {/* Default route */}
        <Route path="/" element={isAuthenticated ? <Navigate to="/home" /> : <Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;