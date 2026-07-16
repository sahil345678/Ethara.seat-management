import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);

    return Promise.reject(
      new Error(
        error.response?.data?.detail ||
        error.response?.data?.message ||
        'An unexpected server error occurred.'
      )
    );
  }
);

export default api;
