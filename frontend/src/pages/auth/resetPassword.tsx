import React from "react";
import { useForm, SubmitHandler } from "react-hook-form";

interface ResetPasswordFormInputs {
  password: string;
  confirmPassword: string;
}

const ResetPasswordForm: React.FC = () => {
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<ResetPasswordFormInputs>();

  const onSubmit: SubmitHandler<ResetPasswordFormInputs> = (data) => {
    console.log(data); // Replace with actual form submission logic
  };

  return (
    <div className="content-section p-6 bg-white rounded-lg shadow-md">
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
    </div>
  );
};

export default ResetPasswordForm;
