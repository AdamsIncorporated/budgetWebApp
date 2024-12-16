import React from "react";
import { Link } from "react-router-dom";
import {
  FaHome,
  FaUser,
  FaSignInAlt,
  FaUserPlus,
  FaKey,
  FaCrown,
  FaCalculator,
} from "react-icons/fa";
import { useSelector, useDispatch } from "react-redux";
import { RootState } from "../../stores/store";
import interceptor from "../../app/axiosConfig";
import { logOut, clearUser } from "../../stores/slices";

interface LinksProps {
  toggleIsOpen: () => void;
}

const Links: React.FC<LinksProps> = ({ toggleIsOpen }) => {
  const dispatch = useDispatch();
  const isAuthenticated = useSelector(
    (state: RootState) => state.auth.isAuthenticated
  );

  const logout = async () => {
    try {
      await interceptor.get("/auth/logout");
      dispatch(logOut());
      dispatch(clearUser());
    } catch (error: any) {
      console.error("Logout failed:", error);
    }
  };

  return (
    <ul className="flex flex-col space-y-4 text-stone-500">
      <li
        className="flex items-center hover:text-stone-800 transition ease-in duration-50"
        onClick={toggleIsOpen}
      >
        <FaHome className="mr-2" />
        <Link to="/">Home</Link>
      </li>

      {isAuthenticated ? (
        <>
          <li
            className="flex items-center hover:text-stone-800 transition ease-in duration-50"
            onClick={toggleIsOpen}
          >
            <FaSignInAlt className="mr-2" />
            <Link to="#" onClick={logout}>Logout</Link>
          </li>
          <li
            className="flex items-center hover:text-stone-800 transition ease-in duration-50"
            onClick={toggleIsOpen}
          >
            <FaUser className="mr-2" />
            <Link to="/auth/account">Account</Link>
          </li>
        </>
      ) : (
        <>
          <li
            className="flex items-center hover:text-stone-800 transition ease-in duration-50"
            onClick={toggleIsOpen}
          >
            <FaSignInAlt className="mr-2" />
            <Link to="/auth/login">Login</Link>
          </li>
          <li
            className="flex items-center hover:text-stone-800 transition ease-in duration-50"
            onClick={toggleIsOpen}
          >
            <FaUserPlus className="mr-2" />
            <Link to="/auth/register">Register</Link>
          </li>
          <li
            className="flex items-center hover:text-stone-800 transition ease-in duration-50"
            onClick={toggleIsOpen}
          >
            <FaKey className="mr-2" />
            <Link to="/auth/reset-password">Reset Password</Link>
          </li>
          <li
            className="flex items-center hover:text-stone-800 transition ease-in duration-50"
            onClick={toggleIsOpen}
          >
            <FaCrown className="mr-2" />
            <Link to="/auth/register-admin/:token">Register Admin</Link>
          </li>
        </>
      )}

      <li
        className="flex items-center hover:text-stone-800 transition ease-in duration-50"
        onClick={toggleIsOpen}
      >
        <FaCalculator className="mr-2" />
        <Link to="/budget/">Budget</Link>
      </li>
      <li
        className="flex items-center hover:text-stone-800 transition ease-in duration-50"
        onClick={toggleIsOpen}
      >
        <FaCalculator className="mr-2" />
        <Link to="/admin-dahsboard/">Admin Dashboard</Link>
      </li>
    </ul>
  );
};

export default Links;
