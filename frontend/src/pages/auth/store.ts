// src/store.ts
import { configureStore, createSlice, PayloadAction } from '@reduxjs/toolkit';

// Define the types for the auth state
interface AuthState {
  isAuthenticated: boolean;
  user: any; // You can replace 'any' with a more specific type if you know the structure of the user object
}

// Initial state for authentication
const initialAuthState: AuthState = {
  isAuthenticated: false,
  user: null,
};

// Create the slice
const authSlice = createSlice({
  name: 'auth',
  initialState: initialAuthState,
  reducers: {
    login(state, action: PayloadAction<any>) {  // Action is a payload with 'any' type, update accordingly
      state.isAuthenticated = true;
      state.user = action.payload;
    },
    logout(state) {
      state.isAuthenticated = false;
      state.user = null;
    },
  },
});

// Configure the store
const store = configureStore({
  reducer: {
    auth: authSlice.reducer,
  },
});

// Export the actions and the store
export default store;
export const { login, logout } = authSlice.actions;
