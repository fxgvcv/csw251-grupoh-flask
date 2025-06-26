import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { createBuilding, getBuildingById, updateBuilding } from '../services/api';

function BuildingForm() {
  const [name, setName] = useState('');
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const { id } = useParams(); // For editing

  useEffect(() => {
    if (id) {
      setIsLoading(true);
      setError(null);
      getBuildingById(id)
        .then(response => {
          setName(response.data.name);
          setIsLoading(false);
        })
        .catch(err => {
          setError(err.message || `Failed to fetch building with id ${id}`);
          console.error(err);
          setIsLoading(false);
        });
    }
  }, [id]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    setError(null);
    const buildingData = { name };

    try {
      if (id) {
        await updateBuilding(id, buildingData);
      } else {
        await createBuilding(buildingData);
      }
      navigate('/buildings');
    } catch (err) {
      setError(err.message || 'Failed to save building');
      console.error(err);
      setIsLoading(false);
    }
  };

  if (isLoading && id) {
    return <p>Loading building data...</p>;
  }

  return (
    <div>
      <h2>{id ? 'Edit Building' : 'Create New Building'}</h2>
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Name:</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Saving...' : 'Save Building'}
        </button>
        <button type="button" onClick={() => navigate('/buildings')} disabled={isLoading}>
          Cancel
        </button>
      </form>
    </div>
  );
}

export default BuildingForm;
