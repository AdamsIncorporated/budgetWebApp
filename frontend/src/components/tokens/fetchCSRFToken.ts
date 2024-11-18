import axios from 'axios';

interface CsrfTokenResponse {
  csrf_token: string;
}

const fetchCSRFToken = async (): Promise<void> => {
  try {
    // Remove any existing CSRF token from localStorage
    localStorage.removeItem('csrf_token');

    // Fetch the new CSRF token
    const response = await axios.get<CsrfTokenResponse>('/api/get-csrf-token');
    const token = response.data.csrf_token;

    // Store the new token in localStorage
    localStorage.setItem('csrf_token', token);

    console.log('CSRF token fetched and stored:', token);
  } catch (error) {
    console.error('Error fetching CSRF token:', error);
  }
};

export default fetchCSRFToken;
