import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import axiosInstance from "../../axiosConfig";
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

interface FormValues {
  is_root_user: boolean;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  password: string;
  confirm_password: string;
}

const RegisterPage: React.FC = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    getValues,
  } = useForm<FormValues>();
  const passwordComplexityRule =
    /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$/;
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        // First GET request
        await axiosInstance.get("/auth/register");
      } catch (error) {
        console.error("Error during login process:", error);
      }
    };

    fetchData();
  }, []);

  const onSubmit = async (data: FormValues) => {
    try {
      const response = await axiosInstance.post("/auth/register", data, {
        headers: {
          "Content-Type": "application/json",
        },
      });
      toast.success(`${data.username} created!`);
      navigate('/auth/login');
    } catch (error: any) {
      const result = error.response?.data || {};
      toast.error(`User creation failed: ${result.message}`);
      console.error("User creation failed", error.response.status);
    }
  };

  return (
    <div className="m-10 h-fit overflow-hidden p-2">
      <div className="flex-col p-6 bg-white rounded-lg shadow-md flex justify-center">
        <form onSubmit={handleSubmit(onSubmit)}>
          <fieldset className="mb-4">
            <legend className="w-full text-3xl text-cyan-700 font-bold border-b pb-2">
              User Registration
            </legend>
            <div className="my-4 border-b pb-2">
              <label className="flex items-center font-bold text-sm">
                <input
                  type="checkbox"
                  id="is_root_user"
                  {...register("is_root_user")}
                  className="form-checkbox h-5 w-5 text-stone-700 transition duration-150 ease-in-out"
                />
                <span className="ml-2 text-stone-700">Create an Admin</span>
              </label>
            </div>

            {/* Username field */}
            <div className="mb-4">
              <label className="block text-stone-700 text-sm font-bold mb-2">
                Username
              </label>
              <input
                type="text"
                {...register("username", { required: "Username is required" })}
                className={`mt-1 block w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400 ${
                  errors.username ? "border-red-500" : "border-gray-300"
                }`}
              />
              {errors.username && (
                <div className="text-red-500 mt-1 text-sm">
                  {errors.username.message}
                </div>
              )}
            </div>

            {/* Email field */}
            <div className="mb-4">
              <label className="block text-stone-700 text-sm font-bold mb-2">
                Email
              </label>
              <input
                type="email"
                {...register("email", { required: "Email is required" })}
                className={`mt-1 block w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400 ${
                  errors.email ? "border-red-500" : "border-gray-300"
                }`}
              />
              {errors.email && (
                <div className="text-red-500 mt-1 text-sm">
                  {errors.email.message}
                </div>
              )}
            </div>

            {/* First Name field */}
            <div className="mb-4">
              <label className="block text-stone-700 text-sm font-bold mb-2">
                First Name
              </label>
              <input
                type="text"
                {...register("first_name", {
                  required: "First name is required",
                })}
                className={`mt-1 block w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400 ${
                  errors.first_name ? "border-red-500" : "border-gray-300"
                }`}
              />
              {errors.first_name && (
                <div className="text-red-500 mt-1 text-sm">
                  {errors.first_name.message}
                </div>
              )}
            </div>

            {/* Last Name field */}
            <div className="mb-4">
              <label className="block text-stone-700 text-sm font-bold mb-2">
                Last Name
              </label>
              <input
                type="text"
                {...register("last_name", {
                  required: "Last name is required",
                })}
                className={`mt-1 block w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400 ${
                  errors.last_name ? "border-red-500" : "border-gray-300"
                }`}
              />
              {errors.last_name && (
                <div className="text-red-500 mt-1 text-sm">
                  {errors.last_name.message}
                </div>
              )}
            </div>

            <div className="mb-4">
              <label className="block text-stone-700 text-sm font-bold mb-2">
                Password
              </label>
              <input
                type="password"
                {...register("password", {
                  required: "Password is required",
                  pattern: {
                    value: passwordComplexityRule,
                    message:
                      "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.",
                  },
                })}
                className={`mt-1 block w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400 ${
                  errors.password ? "border-red-500" : "border-gray-300"
                }`}
              />
              {errors.password && (
                <div className="text-red-500 mt-1 text-sm">
                  {errors.password.message}
                </div>
              )}
            </div>

            <div className="mb-4">
              <label className="block text-stone-700 text-sm font-bold mb-2">
                Confirm Password
              </label>
              <input
                type="password"
                {...register("confirm_password", {
                  required: "Please confirm your password",
                  validate: (value) =>
                    value === getValues("password") || "Passwords must match",
                })}
                className={`mt-1 block w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400 ${
                  errors.confirm_password ? "border-red-500" : "border-gray-300"
                }`}
              />
              {errors.confirm_password && (
                <div className="text-red-500 mt-1 text-sm">
                  {errors.confirm_password.message}
                </div>
              )}
            </div>

            <div className="mb-4">
              <button
                type="submit"
                className="bg-teal-500 text-white font-bold py-2 px-4 rounded hover:bg-teal-600 focus:outline-none focus:ring-2 focus:ring-teal-400"
              >
                Create User
              </button>
            </div>
          </fieldset>
        </form>

        <div className="border-t pt-3 mt-4">
          <small className="text-gray-600">
            Already Have An Account?{" "}
            <a
              className="text-teal-500 hover:text-teal-600 ml-2"
              href="/auth/login"
            >
              Sign In
            </a>
          </small>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
