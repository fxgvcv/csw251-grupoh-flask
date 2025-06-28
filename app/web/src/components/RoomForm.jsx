import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { createRoom, getRoomById, updateRoom, getAllBuildings } from '../services/api';

function RoomForm() {
  const [name, setName] = useState('');
  const [buildingId, setBuildingId] = useState('');
  const [capacity, setCapacity] = useState('');
  const [buildings, setBuildings] = useState([]);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const { id } = useParams(); // For editing

  useEffect(() => {
    setIsLoading(true);
    getAllBuildings()
      .then(response => {
        setBuildings(response.data);
        if (response.data.length > 0 && !id) { // Set default building for new rooms
          setBuildingId(response.data[0].id);
        }
      })
      .catch(err => {
        setError(err.message || 'Failed to fetch buildings');
        console.error(err);
      })
      .finally(() => {
        // If editing, fetch room data after buildings are loaded
        if (id) {
          fetchRoomData();
        } else {
          setIsLoading(false);
        }
      });
  }, [id]); // Rerun if ID changes (though typically it won't for a mounted component)

  const fetchRoomData = () => {
    getRoomById(id)
      .then(response => {
        const room = response.data;
        setName(room.name);
        setBuildingId(room.building_id);
        setCapacity(room.capacity);
      })
      .catch(err => {
        setError(err.message || `Failed to fetch room with id ${id}`);
        console.error(err);
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!buildingId) {
        setError("Please select a building.");
        return;
    }
    setIsLoading(true);
    setError(null);
    const roomData = {
        name,
        building_id: parseInt(buildingId, 10),
        capacity: parseInt(capacity, 10)
    };

    try {
      if (id) {
        await updateRoom(id, roomData);
      } else {
        await createRoom(roomData);
      }
      navigate('/rooms');
    } catch (err) {
      setError(err.message || 'Failed to save room');
      console.error(err);
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <p>Loading form data...</p>;
  }

  return (
    <article>
      <header>
        <h2>{id ? 'Edit Room' : 'Create New Room'}</h2>
      </header>
      {error && <p role="alert">{error}</p>}
      <form onSubmit={handleSubmit}>
        <label htmlFor="name">
          Name:
          <input
            type="text"
            id="name"
            name="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            aria-busy={isLoading && id && !name} // Busy if loading existing data and name isn't populated yet
          />
        </label>

        <label htmlFor="building">
          Building:
          <select
            id="building"
            name="building"
            value={buildingId}
            onChange={(e) => setBuildingId(e.target.value)}
            required
            aria-busy={isLoading && buildings.length === 0} // Busy if buildings are still loading
          >
            <option value="" disabled={buildings.length > 0}>
              {buildings.length === 0 && isLoading ? "Loading buildings..." : "Select a building"}
            </option>
            {buildings.map(building => (
              <option key={building.id} value={building.id}>
                {building.name}
              </option>
            ))}
          </select>
        </label>

        <label htmlFor="capacity">
          Capacity:
          <input
            type="number"
            id="capacity"
            name="capacity"
            value={capacity}
            onChange={(e) => setCapacity(e.target.value)}
            required
            min="0"
            aria-busy={isLoading && id && !capacity} // Busy if loading existing data and capacity isn't populated
          />
        </label>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginTop: '1rem' }}>
          <button type="submit" aria-busy={isLoading} disabled={isLoading}>
            Save Room
          </button>
          <button type="button" className="secondary" onClick={() => navigate('/rooms')} disabled={isLoading}>
            Cancel
          </button>
        </div>
      </form>
    </article>
  );
}

export default RoomForm;
