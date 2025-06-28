import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import BuildingList from './components/BuildingList';
import BuildingForm from './components/BuildingForm';
import RoomList from './components/RoomList';
import RoomForm from './components/RoomForm';
import Login from './components/Login'; 
import './App.css'; 

import client from './services/api'; 

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('userToken');
    if (token) {
      setIsAuthenticated(true);
      client.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }
  }, []);

  const handleLoginSuccess = () => {
    setIsAuthenticated(true);
    const token = localStorage.getItem('userToken');
    if (token) {
      client.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('userToken');
    localStorage.removeItem('username');
    delete client.defaults.headers.common['Authorization'];
    setIsAuthenticated(false); 
  };

  return (
    <Router>
      <nav className="container-fluid">
        <ul>
          <li><strong>SARC</strong></li>
        </ul>
        <ul>
          {isAuthenticated ? (
            <>
              <li>
                <Link to="/buildings">Buildings</Link>
              </li>
              <li>
                <Link to="/rooms">Rooms</Link>
              </li>
              <li>
                <a href="#" onClick={handleLogout} role="button" className="secondary outline">Logout</a>
              </li>
            </>
          ) : (
            <li>
              <Link to="/login" role="button">Login</Link>
            </li>
          )}
        </ul>
      </nav>

      <main className="container">
        <Routes>
          {/* Rota de Login */}
          <Route path="/login" element={isAuthenticated ? <Navigate replace to="/buildings" /> : <Login onLoginSuccess={handleLoginSuccess} />} />

          {/* Rotas protegidas  */}
          <Route
            path="/buildings"
            element={isAuthenticated ? <BuildingList /> : <Navigate replace to="/login" />}
          />
          <Route
            path="/buildings/new"
            element={isAuthenticated ? <BuildingForm /> : <Navigate replace to="/login" />}
          />
          <Route
            path="/buildings/edit/:id"
            element={isAuthenticated ? <BuildingForm /> : <Navigate replace to="/login" />}
          />

          <Route
            path="/rooms"
            element={isAuthenticated ? <RoomList /> : <Navigate replace to="/login" />}
          />
          <Route
            path="/rooms/new"
            element={isAuthenticated ? <RoomForm /> : <Navigate replace to="/login" />}
          />
          <Route
            path="/rooms/edit/:id"
            element={isAuthenticated ? <RoomForm /> : <Navigate replace to="/login" />}
          />

          {/* Rota padrão: redireciona para login se não autenticado, senão para buildings */}
          <Route
            path="*"
            element={isAuthenticated ? <Navigate replace to="/buildings" /> : <Navigate replace to="/login" />}
          />
        </Routes>
      </main>
    </Router>
  );
}

export default App;