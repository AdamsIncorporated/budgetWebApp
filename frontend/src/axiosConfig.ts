import axios from 'axios';

// Create an Axios instance
const axiosInstance = axios.create({
  baseURL: 'http://localhost:5000',
});

// Set up an Axios interceptor to attach CSRF token to every request
axiosInstance.interceptors.request.use(
  (config) => {
    // Get CSRF token from localStorage, state, or context
    const csrfToken = localStorage.getItem('csrfToken');
    if (csrfToken) {
      config.headers['X-CSRF-Token'] = csrfToken;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default axiosInstance;
