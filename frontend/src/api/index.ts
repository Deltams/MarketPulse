import axios from 'axios';

const api = axios.create({
  baseURL: 'http://89.169.179.160:8000/api/v1/',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;