import axios from 'axios';

// Define the type for the response from the API
interface CsrfTokenResponse {
  csrfToken: string;
}

// Define the function to fetch CSRF token and store it in localStorage
const fetchCSRFToken = async (): Promise<void> => {
  try {
    // Send request to the server to get the CSRF token
    const response = await axios.get<CsrfTokenResponse>('/api/csrf-token');
    
    // Extract the token from the response data
    const token = response.data.csrfToken;
    
    // Store the token in localStorage
    localStorage.setItem('csrfToken', token);
    
    console.log('CSRF token fetched and stored:', token); // Debug log (optional)
  } catch (error) {
    console.error('Error fetching CSRF token:', error);
  }
};

export default fetchCSRFToken;
