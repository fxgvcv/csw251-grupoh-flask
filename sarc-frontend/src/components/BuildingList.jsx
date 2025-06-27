import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { getAllBuildings, deleteBuilding as apiDeleteBuilding } from '../services/api';
import ConfirmModal from './ConfirmModal'; // Import the modal

function BuildingList() {
  const [buildings, setBuildings] = useState([]);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true); // Ensure isLoading is initialized
  const navigate = useNavigate();

  // State for modal
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [deleteCandidateId, setDeleteCandidateId] = useState(null);

  useEffect(() => {
    fetchBuildings();
  }, []);

  const fetchBuildings = async () => {
    setIsLoading(true); // Set loading true at the start
    setError(null);
    try {
      const response = await getAllBuildings();
      setBuildings(response.data);
    } catch (err) {
      setError(err.message || 'Failed to fetch buildings');
      console.error(err);
    } finally {
      setIsLoading(false); // Set loading false at the end
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
        await apiDeleteBuilding(deleteCandidateId);
        fetchBuildings(); // Refresh the list
      } catch (err) {
        setError(err.message || 'Failed to delete building');
        console.error(err);
      } finally {
        closeDeleteModal();
        setIsLoading(false); // Stop loading indication
      }
    }
  };

  return (
    <article>
      <header>
        <h2>Buildings</h2>
        <Link to="/buildings/new" role="button">Create New Building</Link>
      </header>
      {error && <p role="alert">{error}</p>}

      {isLoading && !isModalOpen && <p aria-busy="true">Loading buildings...</p>} {/* Hide list loading if modal is open */}

      {buildings.length === 0 && !error && !isLoading && <p>No buildings found.</p>}

      {!isLoading || buildings.length > 0 ? ( // Render table if not loading OR if there's data (even while modal might cause re-fetch)
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {buildings.map((building) => (
              <tr key={building.id}>
                <td>{building.name}</td>
                <td>
                  <button className="outline" onClick={() => navigate(`/buildings/edit/${building.id}`)} style={{ marginRight: '5px' }}>Edit</button>
                  <button className="secondary" onClick={() => openDeleteModal(building.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : null}
      <ConfirmModal
        isOpen={isModalOpen}
        title="Delete Building"
        message={`Are you sure you want to delete building ID ${deleteCandidateId}? This action cannot be undone.`}
        onConfirm={confirmDelete}
        onCancel={closeDeleteModal}
      />
    </article>
  );
}

export default BuildingList;
