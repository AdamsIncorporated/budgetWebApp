import { createSlice, createAsyncThunk, PayloadAction } from "@reduxjs/toolkit";

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

const initialState: AuthState = {
  isAuthenticated: false,
  user: null,
};

export const fetchUser = createAsyncThunk(
  "auth/fetchUser",
  async (userId: number) => {
    const response = await fetch(`/api/users/${userId}`);
    const user = await response.json();
    return user;
  }
);

export const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    logIn(state) {
      state.isAuthenticated = true;
      state.user = {
        id: 0,
        username: "",
        email: "",
        image_file: new Blob([]),
        first_name: "",
        last_name: "",
        is_root_user: false,
      };
    },
    logOut(state) {
      state.isAuthenticated = false;
      state.user = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchUser.fulfilled, (state, action) => {
        state.user = action.payload;
      })
      .addCase(fetchUser.rejected, (state, action) => {
        // Handle error, e.g., show error message
        console.error("Failed to fetch user:", action.error);
      });
  },
});

export const { logIn, logOut } = authSlice.actions;
export default authSlice.reducer;
