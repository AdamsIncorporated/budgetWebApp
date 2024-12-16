import { createSlice, PayloadAction } from "@reduxjs/toolkit";

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

export const { setToken, clearToken } = csrfSlice.actions;
export default csrfSlice.reducer;

