import React, { useLayoutEffect, useState } from "react";
import { useForm, SubmitHandler } from "react-hook-form";
import interceptor from "../../config/axiosConfig";
import { FaEye, FaEyeSlash } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import {
  isPasswordComplex,
  passwordErrorValidationMessage,
} from "../../utils/passwordComplexity";

interface ResetPasswordFormInputs {
  password: string;
  confirm_password: string;
}

const ResetPasswordPage: React.FC = () => {
  const [error, setError] = useState<string | null>(null);
  const [isPageReady, setIsPageReady] = useState<boolean>(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const navigate = useNavigate();
  const pathParts = window.location.pathname.split("/");
  const token = pathParts[pathParts.length - 1];
  const {
    register,
    handleSubmit,
    getValues,
    formState: { errors },
  } = useForm<ResetPasswordFormInputs>();

  useLayoutEffect(() => {
    const fetchData = async () => {
      try {
        await interceptor.get(`/auth/reset-password/${token}`);
        setIsPageReady(true); // Data fetched successfully, set page as ready
      } catch (error) {
        console.error("Error during password reset process:", error);
        setError("An error occurred, please send another reset email."); // Set error message
        setIsPageReady(true); // Done loading even if there was an error
      }
    };

    fetchData();
  }, []);

  const onSubmit: SubmitHandler<ResetPasswordFormInputs> = async (data) => {
    try {
      const response = await interceptor.post(
        `/auth/reset-password/${token}`,
        data,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      toast.success("Password reset!");
      navigate("/auth/login");
    } catch (error: any) {
      const result = error.response?.data || {};
      toast.error(`Password reset failed ${result.message}`);
      console.error("Password reset failed", error.response.status);
    }
  };

  // Only render content after the data is fetched and page is ready
  if (!isPageReady) return null;

  return (
    <div className="m-10 p-6 bg-white rounded-lg shadow-md">
      {error ? (
        <div className="text-3xl font-bold text-rose-500 mb-4">
          <span>{error}</span>
        </div>
      ) : (
        <form onSubmit={handleSubmit(onSubmit)}>
          <fieldset className="mb-4">
            <legend className="text-lg font-bold border-b pb-2">
              Reset Password
            </legend>

            <div className="mb-4">
              <label className="block text-stone-700 text-sm font-bold mb-2">
                Password
              </label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  {...register("password", {
                    required: "Password is required",
                    validate: (value) =>
                      isPasswordComplex(value) ||
                      passwordErrorValidationMessage,
                  })}
                  className={`mt-1 block w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400 ${
                    errors.password ? "border-red-500" : "border-gray-300"
                  }`}
                />
                <button
                  type="button"
                  className="absolute right-2 top-1/2 transform -translate-y-1/2 text-teal-500"
                  onClick={() => setShowPassword((prev) => !prev)}
                >
                  {showPassword ? <FaEyeSlash /> : <FaEye />}
                </button>
              </div>
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
              <div className="relative">
                <input
                  type={showConfirmPassword ? "text" : "password"} // Toggle type based on state
                  {...register("confirm_password", {
                    required: "Please confirm your password",
                    validate: (value) =>
                      value === getValues("password") || "Passwords must match",
                  })}
                  className={`mt-1 block w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400 ${
                    errors.confirm_password
                      ? "border-red-500"
                      : "border-gray-300"
                  }`}
                />
                <button
                  type="button"
                  className="absolute right-2 top-1/2 transform -translate-y-1/2 text-teal-500"
                  onClick={() => setShowConfirmPassword((prev) => !prev)} // Toggle confirm password visibility
                >
                  {showConfirmPassword ? <FaEyeSlash /> : <FaEye />}
                </button>
              </div>
              {errors.confirm_password && (
                <div className="text-red-500 mt-1 text-sm">
                  {errors.confirm_password.message}
                </div>
              )}
            </div>
          </fieldset>

          <div>
            <button
              type="submit"
              className="bg-teal-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-teal-600 focus:outline-none focus:ring-2 focus:ring-teal-400"
            >
              Submit
            </button>
          </div>
        </form>
      )}
    </div>
  );
};

export default ResetPasswordPage;
