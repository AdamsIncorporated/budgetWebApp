import { createSlice, createAction, PayloadAction } from "@reduxjs/toolkit";

const initialAuthState = {
  isAuthenticated: false,
};

const authSlice = createSlice({
  name: "auth",
  initialState: initialAuthState,
  reducers: {
    logIn(state) {
      state.isAuthenticated = true;
    },
    logOut(state) {
      state.isAuthenticated = false;
    },
  },
});

export interface User {
  id: number;
  username: string;
  email: string;
  image_file: Blob;
  first_name: string;
  last_name: string;
  is_root_user: boolean;
}

export interface UserState {
  user: User | null;
}

const initialState: UserState = {
  user: null,
};

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    setUser(state, action: PayloadAction<Partial<User>>) {
      state.user = {
        id: action.payload.id ?? 0,
        username: action.payload.username ?? "",
        email: action.payload.email ?? "",
        image_file:
          action.payload.image_file instanceof Blob
            ? action.payload.image_file
            : new Blob([]),
        first_name: action.payload.first_name ?? "",
        last_name: action.payload.last_name ?? "",
        is_root_user: action.payload.is_root_user ?? false,
      };
    },
    clearUser(state) {
      state.user = null;
    },
  },
});

const initialCsrfState: { token: string | null } = {
  token: null,
};

// Create a CSRF slice
const csrfSlice = createSlice({
  name: "csrf",
  initialState: initialCsrfState,
  reducers: {
    setToken(state, action: PayloadAction<string | null>) {
      state.token = action.payload;
    },
    clearToken(state) {
      state.token = null;
    },
  },
});

// Create a global reset action
export const resetStore = createAction("app/reset");

// Export slices and their actions
export const authReducer = authSlice.reducer;
export const { logIn, logOut } = authSlice.actions;

export const userReducer = userSlice.reducer;
export const { setUser, clearUser } = userSlice.actions;

export const csrfReducer = csrfSlice.reducer;
export const { setToken, clearToken } = csrfSlice.actions;
