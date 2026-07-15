import axios from 'axios';

/**
 * Axios instance pre-configured to communicate with the FastAPI backend.
 * The baseURL points to the /api/v1 prefix.
 * Vite's proxy automatically routes this to localhost:8000 during development.
 */
const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Log API errors globally for debugging
    console.error('API Error:', error.response?.data || error.message);
    
    // Return a standardized error object matching our backend AppException structure
    const customError = new Error(
      error.response?.data?.detail || error.response?.data?.message || 'An unexpected server error occurred.'
    );
    return Promise.reject(customError);
  }
);

export default api;
