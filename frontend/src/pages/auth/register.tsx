import React, { useEffect } from "react";
import { useForm } from "react-hook-form";
import axiosInstance from "../../axiosConfig";

interface FormValues {
  isRootUser: boolean;
  username: string;
  email: string;
  firstName: string;
  lastName: string;
  password: string;
  confirmPassword: string;
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

  const onSubmit = (data: FormValues) => {
    // Handle form submission logic
    console.log("Form submitted", data);
  };

  return (
    <div className="flex justify-center items-center h-fit overflow-hidden p-2">
      <div className="flex-col content-section p-6 bg-white rounded-lg shadow-md w-1/3 flex justify-center">
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
                  {...register("isRootUser")}
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
                {...register("firstName", {
                  required: "First name is required",
                })}
                className={`mt-1 block w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400 ${
                  errors.firstName ? "border-red-500" : "border-gray-300"
                }`}
              />
              {errors.firstName && (
                <div className="text-red-500 mt-1 text-sm">
                  {errors.firstName.message}
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
                {...register("lastName", { required: "Last name is required" })}
                className={`mt-1 block w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400 ${
                  errors.lastName ? "border-red-500" : "border-gray-300"
                }`}
              />
              {errors.lastName && (
                <div className="text-red-500 mt-1 text-sm">
                  {errors.lastName.message}
                </div>
              )}
            </div>

            {/* Password field */}
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

            {/* Confirm Password field */}
            <div className="mb-4">
              <label className="block text-stone-700 text-sm font-bold mb-2">
                Confirm Password
              </label>
              <input
                type="password"
                {...register("confirmPassword", {
                  required: "Please confirm your password",
                  validate: (value) =>
                    value === getValues("password") || "Passwords must match",
                })}
                className={`mt-1 block w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400 ${
                  errors.confirmPassword ? "border-red-500" : "border-gray-300"
                }`}
              />
              {errors.confirmPassword && (
                <div className="text-red-500 mt-1 text-sm">
                  {errors.confirmPassword.message}
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
