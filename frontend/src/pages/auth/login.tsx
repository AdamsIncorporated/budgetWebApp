import React, { useEffect } from "react";
import { useForm } from "react-hook-form";
import fetchCsrfToken from "../../components/tokens/fetchCSRFToken";

interface LoginFormData {
  email: string;
  password: string;
  remember: boolean;
}

const LoginPage: React.FC = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    defaultValues: {
      email: "",
      password: "",
      remember: false,
    },
  });

  useEffect(() => {
    const fetchToken = async () => {
      await fetchCsrfToken(); // This fetches and stores the CSRF token
    };
    fetchToken();
  }, []);

  const onSubmit = async (data: LoginFormData) => {
    console.log("Form Submitted", data);

    try {
      const response = await fetch("/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        const result = await response.json();
        console.log("Login successful", result);
        // Handle successful login (e.g., redirect to dashboard)
      } else {
        console.error("Login failed", response.status);
        // Handle error (e.g., show error message to user)
      }
    } catch (error) {
      console.error("Error during login:", error);
      // Handle network or other errors
    }
  };

  return (
    <div className="bg-gradient-to-r from-teal-50 to-teal-200 flex items-center justify-center min-h-screen swirl">
      <div className="bg-white rounded-lg shadow-md p-8 w-full max-w-md">
        <h2 className="text-2xl font-semibold text-center text-teal-600 mb-6">
          <i className="fas fa-crown"></i> Admin User Login
        </h2>
        <div className="mb-4 text-center">
          <a href="/" className="text-teal-600 hover:underline">
            <i className="fas fa-arrow-left"></i> Back
          </a>
        </div>
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="mb-4">
            <label
              htmlFor="email"
              className="block text-sm font-medium text-gray-700"
            >
              Email
            </label>
            <input
              type="email"
              id="email"
              {...register("email", {
                required: "Email is required",
                pattern: { value: /^\S+@\S+\.\S+$/, message: "Invalid email" },
              })}
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500"
            />
            {errors.email && (
              <div className="text-rose-600 text-sm mt-1">
                {errors.email.message}
              </div>
            )}
          </div>

          <div className="mb-4">
            <label
              htmlFor="password"
              className="block text-sm font-medium text-gray-700"
            >
              Password
            </label>
            <input
              type="password"
              id="password"
              {...register("password", { required: "Password is required" })}
              className="mt-1 block w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500"
            />
            {errors.password && (
              <div className="text-rose-600 text-sm mt-1">
                {errors.password.message}
              </div>
            )}
            <div className="mt-1 text-sm text-teal-600 hover:underline">
              <a href="/auth/reset_request">Forgot Password?</a>
            </div>
          </div>

          <div className="mb-4">
            <div className="form-check">
              <input
                type="checkbox"
                id="remember"
                {...register("remember")}
                className="mr-2"
              />
              <label htmlFor="remember" className="text-sm">
                Remember me
              </label>
            </div>
          </div>

          <div className="mb-4">
            <button
              type="submit"
              className="w-full p-2 bg-teal-600 text-white rounded-md hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-teal-500"
            >
              Login
            </button>
          </div>
        </form>

        <div className="mt-6 text-center">
          <a
            href="/auth/register"
            className="text-sm text-teal-600 hover:underline"
          >
            Create a new account
          </a>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
