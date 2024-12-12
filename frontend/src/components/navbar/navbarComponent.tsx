import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { logOut } from "../../redux/slices";
import { selectCurrentUser } from "../../redux/store";
import SidebarComponent from "../sidebar/sidebarComponent";

const NavbarComponent: React.FC = () => {
  const dispatch = useDispatch();

  // Get the auth state from Redux store
  const isAuthenticated = useSelector(
    (state: any) => state.auth.isAuthenticated
  );
  const currentUser = useSelector(selectCurrentUser);
  const imageUrl =
    currentUser?.image_file instanceof Blob
      ? URL.createObjectURL(currentUser.image_file)
      : "default-avatar.png";

  useEffect(() => {
    // Resetting user-related data when the component mounts
    if (!isAuthenticated) {
      dispatch(logOut());
    }
  }, [isAuthenticated, dispatch]);

  const handleLogin = () => {};

  return (
    <header
      id="navbar"
      className="fixed h-fit top-0 left-0 w-full bg-gradient-to-r from-cyan-500 to-teal-700 text-white p-4 shadow-lg transform translate-y-0"
    >
      <div className="mx-auto flex justify-between items-end">
        <SidebarComponent />
        <div className="flex-col">
          {isAuthenticated ? (
            <div className="flex items-end shadow-md rounded-md p-4">
              <div className="flex justify-center items-center rounded-full w-10 h-10 object-cover mr-4 border-4 border-white bg-cyan-900 text-gray-white">
                <img
                  className="rounded-full w-full h-full object-cover text-xs"
                  src={imageUrl}
                  alt="User Image"
                  onError={(e) => {
                    const target = e.target as HTMLImageElement;
                    target.style.display = "none";
                  }}
                />
              </div>
              <div className="flex-col">
                <h2 className="truncate text-lg font-bold whitespace-nowrap">
                  {currentUser?.is_root_user ? (
                    <span className="text-amber-400">
                      <i className="fas fa-crown"></i> {currentUser?.username}
                    </span>
                  ) : (
                    <span className="text-emerald-400">
                      <i className="fas fa-key"></i> {currentUser?.username}
                    </span>
                  )}
                </h2>
                <p className="truncate break-words">{currentUser?.email}</p>
              </div>
            </div>
          ) : (
            <button
              id="loginBtn"
              className="bg-cyan-600 text-white font-semibold py-2 px-4 rounded transition duration-300 hover:bg-cyan-700 hover:shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-cyan-500"
              onClick={handleLogin}
            >
              <i className="fas fa-sign-in-alt mr-2"></i> Login
            </button>
          )}
        </div>
      </div>
    </header>
  );
};

export default NavbarComponent;
