import {
  configureStore,
  combineReducers,
  createAction,
} from "@reduxjs/toolkit";
import authReducer from "./slices/authSlice";
import csrfReducer from "./slices/csrfSlice";
import { persistStore, persistReducer } from "redux-persist";
import storage from "redux-persist/lib/storage"; // Uses localStorage as default storage

declare global {
  interface Window {
    __REDUX_DEVTOOLS_EXTENSION__: any;
  }
}

// Combine reducers
const combinedReducer = combineReducers({
  auth: authReducer,
  csrf: csrfReducer,
});

// Define the resetStore action
export const resetStore = createAction("resetStore");

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
  devTools:
    process.env.NODE_ENV !== "production" && window.__REDUX_DEVTOOLS_EXTENSION__
      ? window.__REDUX_DEVTOOLS_EXTENSION__()
      : undefined,
});

// Persistor for the store
const persistor = persistStore(store);

export { store, persistor };
