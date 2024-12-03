import React from "react";
import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Provider } from "react-redux";
import { PersistGate } from "redux-persist/integration/react";
import { ToastContainer } from "react-toastify";

import IndexPage from "./pages/index";
import LoginPage from "./pages/auth/login";
import AccountPage from "./pages/auth/account";
import RegisterPage from "./pages/auth/register";
import RequestResetPasswordPage from "./pages/auth/requestResetPassword";
import { store, persistor } from "./redux/store";

const App: React.FC = () => {
  return (
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <Router future={{ v7_relativeSplatPath: true, v7_startTransition: true }}>
          <Routes>
            <Route path="/" element={<IndexPage />} />
            <Route path="/auth/login" element={<LoginPage />} />
            <Route path="/auth/account" element={<AccountPage />} />
            <Route path="/auth/register" element={<RegisterPage />} />
            <Route path="/auth/reset-password" element={<RequestResetPasswordPage />} />
          </Routes>
          <ToastContainer />
        </Router>
      </PersistGate>
    </Provider>
  );
};

export default App;
