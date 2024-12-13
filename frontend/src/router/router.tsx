import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Header from "../components/navbar/Header";
import Footer from "../components/footer/Footer";
import { ToastContainer } from "react-toastify";


import HomePage from "../pages/index/home";
import LoginPage from "../pages/auth/login";
import AccountPage from "../pages/auth/login";
import RegisterPage from "../pages/auth/register";
import RegisterAdminPage from "../pages/auth/registerAdmin";
import RequestResetPasswordPage from "../pages/auth/requestResetPassword";
import ResetPasswordPage from "../pages/auth/resetPassword";

// Layout elements must be placed within BrowserRouter element such as Navbar and ToastContainer
const Router = () => (
  <BrowserRouter
    future={{ v7_relativeSplatPath: true, v7_startTransition: true }}
  >
    <Header />
    <div id="main">
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/auth">
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
    </div>
    <ToastContainer />
    <Footer/>
  </BrowserRouter>
);

export default Router;
