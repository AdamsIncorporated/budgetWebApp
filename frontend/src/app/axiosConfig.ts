import axios from "axios";
import { setToken, clearToken } from "../stores/slices/csrfSlice";
import { store } from "../stores/store";

// Function to get the CSRF token from the Redux store
const getCsrfTokenFromStore = (): string | null => {
  const state = store.getState();
  return state.csrf.token;
};

// Create an Axios instance
const interceptor = axios.create({
  baseURL: "/api",
  withCredentials: true,
});

// Add the CSRF token to request headers before each request
interceptor.interceptors.request.use(
  (config) => {
    const csrfToken = getCsrfTokenFromStore();

    if (csrfToken) {
      config.headers["x-csrftoken"] = csrfToken;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle CSRF token in the response headers
interceptor.interceptors.response.use(
  (response) => {
    // Check if the CSRF token is present in the response headers
    const csrfToken = response.headers["x-csrftoken"];

    if (csrfToken) {
      console.log("CSRF token received from response, updating Redux store");

      // Remove any existing token in Redux store
      store.dispatch(clearToken());

      // Store the new CSRF token in Redux
      store.dispatch(setToken(csrfToken));
    }

    return response;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default interceptor;
