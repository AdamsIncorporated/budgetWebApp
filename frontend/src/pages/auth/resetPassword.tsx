import React, { useLayoutEffect, useState } from "react";
import { useForm, SubmitHandler } from "react-hook-form";
import axiosInstance from "../../axiosConfig";

interface ResetPasswordFormInputs {
  password: string;
  confirmPassword: string;
}

const ResetPasswordPage: React.FC = () => {
  const [error, setError] = useState<string | null>(null); // Track error state
  const [isPageReady, setIsPageReady] = useState<boolean>(false); // Track if page is ready

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<ResetPasswordFormInputs>();

  useLayoutEffect(() => {
    const fetchData = async () => {
      try {
        const pathParts = window.location.pathname.split("/");
        const token = pathParts[pathParts.length - 1];
        await axiosInstance.get(`/auth/reset-password/${token}`);
        setIsPageReady(true); // Data fetched successfully, set page as ready
      } catch (error) {
        console.error("Error during password reset process:", error);
        setError("An error occurred, please send another reset email."); // Set error message
        setIsPageReady(true); // Done loading even if there was an error
      }
    };

    fetchData();
  }, []);

  const onSubmit: SubmitHandler<ResetPasswordFormInputs> = (data) => {
    console.log(data);
  };

  // Only render content after the data is fetched and page is ready
  if (!isPageReady) return null; // Don't render anything until ready

  return (
    <div className="m-10 p-6 bg-white rounded-lg shadow-md">
      {error ? (
        <div className="text-red-500 mb-4">
          <span>{error}</span>
        </div>
      ) : (
        <form onSubmit={handleSubmit(onSubmit)}>
          <fieldset className="mb-4">
            <legend className="text-lg font-bold border-b pb-2">
              Reset Password
            </legend>

            <div className="mb-4">
              <label
                htmlFor="password"
                className="block text-gray-700 text-sm font-bold mb-2"
              >
                Password
              </label>
              <input
                type="password"
                id="password"
                {...register("password", { required: "Password is required" })}
                className={`mt-1 block w-full p-2 border ${
                  errors.password ? "border-red-500" : "border-gray-300"
                } rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400`}
              />
              {errors.password && (
                <div className="text-red-500 mt-1 text-sm">
                  <span>{errors.password.message}</span>
                </div>
              )}
            </div>

            <div className="mb-4">
              <label
                htmlFor="confirmPassword"
                className="block text-gray-700 text-sm font-bold mb-2"
              >
                Confirm Password
              </label>
              <input
                type="password"
                id="confirmPassword"
                {...register("confirmPassword", {
                  required: "Confirm Password is required",
                  validate: (value) =>
                    value === watch("password") || "Passwords do not match",
                })}
                className={`mt-1 block w-full p-2 border ${
                  errors.confirmPassword ? "border-red-500" : "border-gray-300"
                } rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400`}
              />
              {errors.confirmPassword && (
                <div className="text-red-500 mt-1 text-sm">
                  <span>{errors.confirmPassword.message}</span>
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
