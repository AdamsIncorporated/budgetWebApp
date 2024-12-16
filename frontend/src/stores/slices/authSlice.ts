import {
  createSlice,
  createAsyncThunk,
  createSelector,
} from "@reduxjs/toolkit";
import { stat } from "fs";

export interface User {
  id: number;
  username: string;
  email: string;
  image_file: Blob;
  first_name: string;
  last_name: string;
  is_root_user: boolean;
}

export interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
}

interface RootState {
  auth: AuthState;
}

const initialState: AuthState = {
  isAuthenticated: false,
  user: null,
};

export const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    logIn(state, action) {
      state.isAuthenticated = true;
      state.user = action.payload;
    },
    logOut(state) {
      state.isAuthenticated = false;
      state.user = null;
    },
  },
});

export const { logIn, logOut } = authSlice.actions;
export const selectIsAuthenticated = createSelector(
  (state: RootState) => state.auth,
  (auth) => auth.isAuthenticated
);
export const selectCurrentUser = createSelector(
  (state: RootState) => state.auth,
  (auth) => auth.user
);
export default authSlice.reducer;
