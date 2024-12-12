import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { ToastContainer } from "react-toastify";

import IndexPage from "../pages/index";
import HomePage from "../pages/index/home";
import LoginPage from "../pages/auth/login";
import AccountPage from "../pages/auth/login";
import RegisterPage from "../pages/auth/register";
import RegisterAdminPage from "../pages/auth/registerAdmin";
import RequestResetPasswordPage from "../pages/auth/requestResetPassword";
import ResetPasswordPage from "../pages/auth/resetPassword";

const Router = () => (
  <BrowserRouter
    future={{ v7_relativeSplatPath: true, v7_startTransition: true }}
  >
    <Routes>
      <Route path="/" element={<IndexPage />}>
        <Route index element={<HomePage />} />
        <Route path="/home" element={<HomePage />} />
      </Route>
      <Route path="/auth" element={<IndexPage />}>
        <Route path="login" element={<LoginPage />} />
        <Route path="account" element={<AccountPage />} />
        <Route path="register" element={<RegisterPage />} />
        <Route path="reset-password" element={<RequestResetPasswordPage />} />
        <Route
          path="reset-password-token/:token"
          element={<ResetPasswordPage />}
        />
        <Route path="register-admin/:token" element={<RegisterAdminPage />} />
      </Route>
    </Routes>
    <ToastContainer />
  </BrowserRouter>
);

export default Router;
