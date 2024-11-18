import React from "react";
import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Provider } from "react-redux";
import { ToastContainer } from "react-toastify";

import IndexPage from "./pages/index";
import LoginPage from "./pages/auth/login";
import store from "./pages/auth/store";
const App: React.FC = () => {
  return (
    <Provider store={store}>
      {" "}
      <Router>
        <Routes>
          <Route path="/" element={<IndexPage />} />
          <Route path="/login" element={<LoginPage />} />
        </Routes>
        <ToastContainer />
      </Router>
    </Provider>
  );
};

export default App;
