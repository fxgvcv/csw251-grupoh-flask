import axios from 'axios';

const API_BASE_URL = ' https://r33grhtvqi.execute-api.us-east-1.amazonaws.com/dev/';

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Building Endpoints
export const getAllBuildings = () => client.get('/buildings/');
export const getBuildingById = (id) => client.get(`/buildings/${id}`);
export const createBuilding = (data) => client.post('/buildings/', data);
export const updateBuilding = (id, data) => client.put(`/buildings/${id}`, data);
export const deleteBuilding = (id) => client.delete(`/buildings/${id}`);

// Room Endpoints
export const getAllRooms = () => client.get('/rooms/');
export const getRoomById = (id) => client.get(`/rooms/${id}`);
export const createRoom = (data) => client.post('/rooms/', data);
export const updateRoom = (id, data) => client.put(`/rooms/${id}`, data);
export const deleteRoom = (id) => client.delete(`/rooms/${id}`);

//Login endpoints
export const registerUser = (userData) => client.post('/users', userData);
export const authenticateUser = (credentials) => client.post('/users/authenticate', credentials);

export default client;
