import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { getAllRooms, deleteRoom as apiDeleteRoom, getAllBuildings } from '../services/api';
import ConfirmModal from './ConfirmModal'; // Import the modal

function RoomList() {
  const [rooms, setRooms] = useState([]);
  const [buildings, setBuildings] = useState({}); // To map building_id to name
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  // State for modal
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [deleteCandidateId, setDeleteCandidateId] = useState(null);

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

  const openDeleteModal = (id) => {
    setDeleteCandidateId(id);
    setIsModalOpen(true);
  };

  const closeDeleteModal = () => {
    setDeleteCandidateId(null);
    setIsModalOpen(false);
  };

  const confirmDelete = async () => {
    if (deleteCandidateId) {
      setIsLoading(true); // Optional: indicate loading during delete
      try {
        await apiDeleteRoom(deleteCandidateId);
        fetchRoomsAndBuildings(); // Refresh the list
      } catch (err) {
        setError(err.message || 'Failed to delete room');
        console.error(err);
      } finally {
        closeDeleteModal();
        // setIsLoading(false); // fetchRoomsAndBuildings will handle this
      }
    }
  };

  return (
    <article>
      <header>
        <h2>Rooms</h2>
        <Link to="/rooms/new" role="button">Create New Room</Link>
      </header>
      {error && <p role="alert">{error}</p>}

      {isLoading && !isModalOpen && <p aria-busy="true">Loading rooms...</p>}

      {rooms.length === 0 && !error && !isLoading && <p>No rooms found.</p>}

      {(!isLoading || rooms.length > 0) && !isModalOpen ? ( // Render table if not loading OR if there's data, and modal isn't hiding it
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Building</th>
              <th>Capacity</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {rooms.map((room) => (
              <tr key={room.id}>
                <td>{room.name}</td>
                <td>{buildings[room.building_id] || 'N/A'}</td>
                <td>{room.capacity}</td>
                <td>
                  <button className="outline" onClick={() => navigate(`/rooms/edit/${room.id}`)} style={{ marginRight: '5px' }}>Edit</button>
                  <button className="secondary" onClick={() => openDeleteModal(room.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : null}
       {!isLoading && rooms.length > 0 && isModalOpen && ( // Keep table visible if modal is open over populated list
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Building</th>
              <th>Capacity</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {rooms.map((room) => (
              <tr key={room.id}>
                <td>{room.name}</td>
                <td>{buildings[room.building_id] || 'N/A'}</td>
                <td>{room.capacity}</td>
                <td>
                  {/* Buttons could be disabled here if preferred while modal is open */}
                  <button className="outline" onClick={() => navigate(`/rooms/edit/${room.id}`)} style={{ marginRight: '5px' }}>Edit</button>
                  <button className="secondary" onClick={() => openDeleteModal(room.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      <ConfirmModal
        isOpen={isModalOpen}
        title="Delete Room"
        message={`Are you sure you want to delete room ID ${deleteCandidateId}? This action cannot be undone.`}
        onConfirm={confirmDelete}
        onCancel={closeDeleteModal}
      />
    </article>
  );
}

export default RoomList;
