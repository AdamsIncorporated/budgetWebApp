import { configureStore, combineReducers } from "@reduxjs/toolkit";
import { authReducer, csrfReducer, userReducer, resetStore } from "./slices";
import { persistStore, persistReducer } from "redux-persist";
import storage from "redux-persist/lib/storage"; // Uses localStorage as default storage

// Combine reducers
const combinedReducer = combineReducers({
  auth: authReducer,
  user: userReducer,
  csrf: csrfReducer,
});

// Root reducer to handle resetting the entire store
const rootReducer = (
  state: ReturnType<typeof combinedReducer> | undefined,
  action: any
) => {
  if (action.type === resetStore.type) {
    state = undefined; // Clear the entire state
  }
  return combinedReducer(state, action);
};

// Configure persist settings
const persistConfig = {
  key: "root",
  storage,
  whitelist: ["auth", "user"],
};

// Persist reducer wrapping the root reducer
const persistedReducer = persistReducer(persistConfig, rootReducer);

// Configure the store
const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        // Ignore Redux Persist actions with non-serializable values
        ignoredActions: ["persist/PERSIST", "persist/REHYDRATE"],
      },
    }),
});


// Persistor for the store
const persistor = persistStore(store);

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export { store, persistor };
export const selectCurrentUser = (state: RootState) => state.user.user;
