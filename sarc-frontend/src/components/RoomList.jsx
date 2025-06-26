import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { getAllRooms, deleteRoom as apiDeleteRoom, getAllBuildings } from '../services/api';

function RoomList() {
  const [rooms, setRooms] = useState([]);
  const [buildings, setBuildings] = useState({}); // To map building_id to name
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchRoomsAndBuildings();
  }, []);

  const fetchRoomsAndBuildings = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const [roomsResponse, buildingsResponse] = await Promise.all([
        getAllRooms(),
        getAllBuildings()
      ]);

      setRooms(roomsResponse.data);

      const buildingsMap = buildingsResponse.data.reduce((acc, building) => {
        acc[building.id] = building.name;
        return acc;
      }, {});
      setBuildings(buildingsMap);

    } catch (err) {
      setError(err.message || 'Failed to fetch data');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this room?')) {
      try {
        await apiDeleteRoom(id);
        // Refetch rooms, buildings might not have changed but it's simpler to refetch both
        fetchRoomsAndBuildings();
      } catch (err) {
        setError(err.message || 'Failed to delete room');
        console.error(err);
      }
    }
  };

  if (isLoading) {
    return <p>Loading rooms...</p>;
  }

  return (
    <div>
      <h2>Rooms</h2>
      <Link to="/rooms/new">Create New Room</Link>
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      {rooms.length === 0 && !error && <p>No rooms found.</p>}
      <ul>
        {rooms.map((room) => (
          <li key={room.id}>
            {room.name} (Building: {buildings[room.building_id] || 'N/A'}, Capacity: {room.capacity})
            <button onClick={() => navigate(`/rooms/edit/${room.id}`)} style={{ marginLeft: '10px' }}>Edit</button>
            <button onClick={() => handleDelete(room.id)} style={{ marginLeft: '5px', color: 'red' }}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default RoomList;
