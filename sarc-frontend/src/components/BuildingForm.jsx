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
    <article>
      <header>
        <h2>{id ? 'Edit Building' : 'Create New Building'}</h2>
      </header>
      {error && <p role="alert">{error}</p>} {/* Using Pico's default alert styling */}
      <form onSubmit={handleSubmit}>
        <label htmlFor="name">
          Name:
          <input
            type="text"
            id="name"
            name="name" // Good practice for forms
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            aria-busy={isLoading && id} // Show busy state when loading existing data
          />
        </label>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
          <button type="submit" aria-busy={isLoading} disabled={isLoading}>
            Save Building
          </button>
          <button type="button" className="secondary" onClick={() => navigate('/buildings')} disabled={isLoading}>
            Cancel
          </button>
        </div>
      </form>
    </article>
  );
}

export default BuildingForm;
