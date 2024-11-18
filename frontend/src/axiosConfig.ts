import axios from 'axios';

// Create an Axios instance
const axiosInstance = axios.create({
  baseURL: 'http://localhost:5000',
});

// Set up an Axios interceptor to attach CSRF token to every request
axiosInstance.interceptors.request.use(
  (config) => {
    // Log the request details
    console.log(`Sending request to ${config.url} with method ${config.method}`);
    
    // Get CSRF token from localStorage
    const csrfToken = localStorage.getItem('csrfToken');
    if (csrfToken) {
      config.headers['X-CSRF-Token'] = csrfToken;
      console.debug(`CSRF token attached: ${csrfToken}`);
    } else {
      console.error('No CSRF token found in localStorage');
    }

    return config;
  },
  (error) => {
    console.error(`Request error: ${error.message}`);
    return Promise.reject(error);
  }
);

// Set up an Axios response interceptor to log the response data
axiosInstance.interceptors.response.use(
  (response) => {
    // Log successful response
    console.info(`Received response from ${response.config.url} with status ${response.status}`);
    console.debug(`Response data: ${JSON.stringify(response.data)}`);
    return response;
  },
  (error) => {
    // Log the error if the response fails
    if (error.response) {
      console.error(`Response error from ${error.response.config.url} with status ${error.response.status}`);
      console.debug(`Error response data: ${JSON.stringify(error.response.data)}`);
    } else {
      console.error(`Network error: ${error.message}`);
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
