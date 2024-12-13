import React, { useEffect } from "react";
import { useForm, SubmitHandler } from "react-hook-form";
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import interceptor from "../../app/axiosConfig";

const RequestResetPasswordPage: React.FC = () => {
  const {
    register,
    handleSubmit,
    formState: { errors: formErrors },
  } = useForm<{ email: string }>();

  useEffect(() => {
    const fetchData = async () => {
      try {
        await interceptor.get("/auth/request-reset-password");
      } catch (error) {
        console.error("Error during login process:", error);
      }
    };

    fetchData();
  }, []);

  const onSubmit: SubmitHandler<{ email: string }> = async (data) => {
    try {
      const response = await interceptor.post(
        "/auth/request-reset-password",
        data,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      toast.success(`${response?.data?.message}`);
    } catch (error: any) {
      const errorMessage =
        error.response?.data?.message || "An unexpected error occurred.";
      toast.error(`Error in sending reset email. ${errorMessage}`);
      console.error("User creation failed", error.response.status);
    }
  };

  return (
    <div className="m-10 p-6 bg-white rounded-lg shadow-md text-cyan-600">
      <form onSubmit={handleSubmit(onSubmit)}>
        <fieldset className="mb-4">
          <legend className="text-3xl font-bold border-b pb-2">
            Reset Password
          </legend>
          <div className="mb-4">
            <label
              className="block text-stone-700 font-bold my-2"
              htmlFor="email"
            >
              Email
            </label>
            <input
              id="email"
              type="email"
              {...register("email", {
                required: "Email is required",
              })}
              className={`text-stone-700 mt-1 block w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400 ${
                formErrors.email ? "border-red-500" : "border-gray-300"
              }`}
            />
            {formErrors.email && (
              <div className="text-red-500 mt-1 text-sm">
                <span>{formErrors.email.message}</span>
              </div>
            )}
          </div>
        </fieldset>
        <div>
          <button
            type="submit"
            className="bg-teal-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-teal-600 focus:outline-none focus:ring-2 focus:ring-teal-400"
          >
            Reset Password
          </button>
        </div>
      </form>
    </div>
  );
};

export default RequestResetPasswordPage;
