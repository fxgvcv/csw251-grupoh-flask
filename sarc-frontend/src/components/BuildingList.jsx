import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { getAllBuildings, deleteBuilding as apiDeleteBuilding } from '../services/api';

function BuildingList() {
  const [buildings, setBuildings] = useState([]);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchBuildings();
  }, []);

  const fetchBuildings = async () => {
    try {
      setError(null);
      const response = await getAllBuildings();
      setBuildings(response.data);
    } catch (err) {
      setError(err.message || 'Failed to fetch buildings');
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this building?')) {
      try {
        await apiDeleteBuilding(id);
        fetchBuildings(); // Refresh the list
      } catch (err) {
        setError(err.message || 'Failed to delete building');
        console.error(err);
      }
    }
  };

  return (
    <div>
      <h2>Buildings</h2>
      <Link to="/buildings/new">Create New Building</Link>
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      {buildings.length === 0 && !error && <p>No buildings found.</p>}
      <ul>
        {buildings.map((building) => (
          <li key={building.id}>
            {building.name}
            <button onClick={() => navigate(`/buildings/edit/${building.id}`)} style={{ marginLeft: '10px' }}>Edit</button>
            <button onClick={() => handleDelete(building.id)} style={{ marginLeft: '5px', color: 'red' }}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default BuildingList;
