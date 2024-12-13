import React, { useEffect, useState } from "react";
import interceptor from "../../config/axiosConfig";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { FaCrown } from "react-icons/fa";

interface UserAdmin {
  username: string;
  first_name: string;
  last_name: string;
}

const RegisterAdminPage: React.FC = () => {
  const [userAdmin, setUserAdmin] = useState<UserAdmin | null>(null);
  const navigate = useNavigate();
  const pathParts = window.location.pathname.split("/");
  const token = pathParts[pathParts.length - 1];

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await interceptor.get(
          `/auth/register-admin/${token}`
        );
        const user = response?.data.user;
        setUserAdmin(user);
      } catch (error: any) {
        const message = error.response?.data.message;
        console.error(message);
        toast.error(message);
      }
    };

    fetchData();
  }, []);

  const onSubmit = async () => {
    try {
      await interceptor.post(`/auth/register-admin/${token}`, {
        headers: {
          "Content-Type": "application/json",
        },
      });
      toast.success("Admin User created!");
      navigate("/auth/login");
    } catch (error: any) {
      const message = error.response?.data.message;
      toast.error("Admin creation failed");
      console.error("Admin creation failed:", message);
    }
  };

  return (
    <div className="m-10 p-6 bg-white rounded-lg shadow-md flex justify-center">
      <div>
        <h1 className="p-5 my-5 text-cyan-700 text-3xl font-bold flex items-end gap-4">
          <FaCrown className="text-amber-500" />
          Confirm Admin Creation
        </h1>
        <table className="my-5 table-auto border-collapse w-full text-lg text-stone-700">
          <tbody>
            <tr className="border-b border-stone-100">
              <td className="p-2 font-bold">Username</td>
              <td className="p-2 flex justify-end">{userAdmin?.username}</td>
            </tr>
            <tr className="border-b border-stone-100">
              <td className="p-2 font-bold">Full Name</td>
              <td className="p-2 flex justify-end">
                {userAdmin?.first_name} {userAdmin?.last_name}
              </td>
            </tr>
          </tbody>
        </table>
        <div className="flex justify-center">
          <button
            type="button"
            className="bg-teal-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-teal-600 focus:outline-none focus:ring-2 focus:ring-teal-400"
            onClick={onSubmit}
          >
            Confirm Admin Creation For {userAdmin?.username}
          </button>
        </div>
      </div>
    </div>
  );
};

export default RegisterAdminPage;
