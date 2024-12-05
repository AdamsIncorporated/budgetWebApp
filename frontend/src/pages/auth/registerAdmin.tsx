import React, { useLayoutEffect, useState } from "react";
import axiosInstance from "../../axiosConfig";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

interface UserAdmin {
  username: string;
  first_name: string;
  last_name: string;
}

const RegisterAdminPage: React.FC = () => {
  const [error, setError] = useState<string | null>(null);
  const [userAdmin, setUserAdmin] = useState<UserAdmin | null>(null);
  const [isPageReady, setIsPageReady] = useState<boolean>(false);
  const navigate = useNavigate();
  const pathParts = window.location.pathname.split("/");
  const token = pathParts[pathParts.length - 1];

  useLayoutEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axiosInstance.get(
          `/auth/register-admin/${token}`
        );
        const user = response?.data.user;
        setUserAdmin(user);
        setIsPageReady(true);
      } catch (error) {
        setError(
          "Error during admin creation process. Please send another email"
        );
        console.error(error);
        setIsPageReady(true);
      }
    };

    fetchData();
  }, []);

  const onSubmit = async () => {
    try {
      await axiosInstance.post(`/auth/reset-password/${token}`, {
        headers: {
          "Content-Type": "application/json",
        },
      });
      toast.success("Admin User created!");
      navigate("/auth/login");
    } catch (error: any) {
      toast.error("Admin creation failed");
      console.error("Admin creation failed:", error.response.status);
    }
  };

  if (!isPageReady) return null;

  return (
    <div className="m-10 p-6 bg-white rounded-lg shadow-md">
      {error ? (
        <div className="text-3xl font-bold text-rose-500 mb-4">
          <span>{error}</span>
        </div>
      ) : (
        <div>
          <div className="text-bold text-cyan-700 text-2xl">
            <span>{userAdmin?.username}</span>
            <span>{userAdmin?.first_name}</span>
            <span>{userAdmin?.last_name}</span>
          </div>
          <form onSubmit={onSubmit}>
            <div>
              <button
                type="submit"
                className="jusitify-center bg-teal-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-teal-600 focus:outline-none focus:ring-2 focus:ring-teal-400"
              >
                Confirm Admin {userAdmin?.username}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};

export default RegisterAdminPage;
