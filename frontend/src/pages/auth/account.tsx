import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { selectCurrentUser } from "../../stores/slices/authSlice";
import interceptor from "../../app/axiosConfig";

interface FormData {
  username: string;
  email: string;
  firstName: string;
  lastName: string;
  picture: File | null;
}

const AccountSettings: React.FC = () => {
  const currentUser = useSelector(selectCurrentUser);
  const id = currentUser?.id

  const [formData, setFormData] = useState<FormData>({
    username: "",
    email: "",
    firstName: "",
    lastName: "",
    picture: null,
  });
  const [errors, setErrors] = useState<Partial<FormData>>({});

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, files } = e.target;
    if (type === "file") {
      setFormData((prevData) => ({
        ...prevData,
        [name]: files ? files[0] : null,
      }));
    } else {
      setFormData((prevData) => ({
        ...prevData,
        [name]: value,
      }));
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        await interceptor.get("/auth/account", { params: { Id: id } });
      } catch (error) {
        console.error("Error during login process:", error);
      }
    };

    fetchData();
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle form submission logic (e.g., validation, API call)
  };

  return (
    <div className="flex justify-center">
      <div className="text-teal-700 content-section p-6 bg-white rounded-lg shadow-md w-1/3 flex-col justify-center overflow-hidden">
        <div className="mb-3 hover:underline">
          <a href="/">
            <i className="fas fa-arrow-left"></i> Back
          </a>
        </div>

        <div className="flex items-center mb-6 border-b border-stone-200 pb-3 w-full">
          <img
            className="rounded-full w-10 h-10 object-cover mr-4"
            src={`data:image/jpeg;base64,${"image_file"}`} // Replace 'image_file' with the actual image data
            alt="User Image"
          />
          <div className="flex-col">
            <h2 className="truncate text-2xl font-bold whitespace-nowrap">
              <span className="text-amber-400">
                <i className="fas fa-crown"></i> Admin
              </span>
              <div>{currentUser?.username}</div>
            </h2>
            <p className="truncate text-stone-500 break-words">
              {currentUser?.email}
            </p>
          </div>
        </div>

        <form onSubmit={handleSubmit} encType="multipart/form-data">
          <fieldset className="mb-4">
            <div className="mb-4">
              <label
                className="block text-sm font-bold mb-2"
                htmlFor="username"
              >
                Username
              </label>
              <input
                type="text"
                id="username"
                name="username"
                value={formData.username}
                onChange={handleChange}
                className={`mt-1 block w-full p-2 border ${
                  errors.username ? "border-red-500" : "border-gray-300"
                } rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400`}
              />
              {errors.username && (
                <div className="text-red-500 mt-1 text-sm">
                  {errors.username}
                </div>
              )}
            </div>

            <div className="mb-4">
              <label className="block text-sm font-bold mb-2" htmlFor="email">
                Email
              </label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className={`mt-1 block w-full p-2 border ${
                  errors.email ? "border-red-500" : "border-gray-300"
                } rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400`}
              />
              {errors.email && (
                <div className="text-red-500 mt-1 text-sm">{errors.email}</div>
              )}
            </div>

            <div className="mb-4">
              <label
                className="block text-sm font-bold mb-2"
                htmlFor="firstName"
              >
                First Name
              </label>
              <input
                type="text"
                id="firstName"
                name="firstName"
                value={formData.firstName}
                onChange={handleChange}
                className={`mt-1 block w-full p-2 border ${
                  errors.firstName ? "border-red-500" : "border-gray-300"
                } rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400`}
              />
              {errors.firstName && (
                <div className="text-red-500 mt-1 text-sm">
                  {errors.firstName}
                </div>
              )}
            </div>

            <div className="mb-4">
              <label
                className="block text-sm font-bold mb-2"
                htmlFor="lastName"
              >
                Last Name
              </label>
              <input
                type="text"
                id="lastName"
                name="lastName"
                value={formData.lastName}
                onChange={handleChange}
                className={`mt-1 block w-full p-2 border ${
                  errors.lastName ? "border-red-500" : "border-gray-300"
                } rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400`}
              />
              {errors.lastName && (
                <div className="text-red-500 mt-1 text-sm">
                  {errors.lastName}
                </div>
              )}
            </div>

            <div className="mb-4 rounded-md border-2 text-teal-700 border-2 border-teal-700 border-dashed p-2">
              <label className="block font-medium mb-2" htmlFor="picture">
                Profile Picture
              </label>
              <input
                type="file"
                id="picture"
                name="picture"
                className="block w-full text-md file:border-none file:text-white file:mr-4 file:py-2 file:px-4 file:rounded-md file:cursor-pointer file:bg-teal-500 hover:file:bg-teal-600"
              />
              {errors.picture && typeof errors.picture === "string" && (
                <div className="text-red-500 mt-1 text-sm">
                  {errors.picture}
                </div>
              )}
            </div>
          </fieldset>

          <div className="flex justify-end">
            <button
              type="submit"
              className="flex items-center justify-center bg-teal-500 text-white font-bold py-2 px-4 rounded hover:bg-teal-600 focus:outline-none focus:ring-2 focus:ring-teal-400 focus:ring-opacity-75"
            >
              <i className="fas fa-paper-plane mr-2"></i> Update
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AccountSettings;
