import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import BuildingList from './components/BuildingList';
import BuildingForm from './components/BuildingForm';
import RoomList from './components/RoomList';
import RoomForm from './components/RoomForm';
import './App.css'; // Basic styling

function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/buildings">Buildings</Link>
            </li>
            <li>
              <Link to="/rooms">Rooms</Link>
            </li>
          </ul>
        </nav>

        <hr />

        <div className="content">
          <Routes>
            {/* Default route */}
            <Route path="/" element={<Navigate replace to="/buildings" />} />

            {/* Building Routes */}
            <Route path="/buildings" element={<BuildingList />} />
            <Route path="/buildings/new" element={<BuildingForm />} />
            <Route path="/buildings/edit/:id" element={<BuildingForm />} />

            {/* Room Routes */}
            <Route path="/rooms" element={<RoomList />} />
            <Route path="/rooms/new" element={<RoomForm />} />
            <Route path="/rooms/edit/:id" element={<RoomForm />} />

            {/* Fallback for unknown routes (optional) */}
            <Route path="*" element={<Navigate replace to="/" />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
