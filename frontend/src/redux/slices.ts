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
  Id: number,
  Username: string;
  Email: string;
  ImageFile: Blob;
  FirstName: string;
  LastName: string;
  IsRootUser: boolean;
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
        Id: action.payload.Id ?? 0,
        Username: action.payload.Username ?? "",
        Email: action.payload.Email ?? "",
        ImageFile:
          action.payload.ImageFile instanceof Blob
            ? action.payload.ImageFile
            : new Blob([]),
        FirstName: action.payload.FirstName ?? "",
        LastName: action.payload.LastName ?? "",
        IsRootUser: action.payload.IsRootUser ?? false,
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
