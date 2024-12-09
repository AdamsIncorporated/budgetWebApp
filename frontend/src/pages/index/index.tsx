import { useNavigate } from "react-router-dom";
import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { logOut } from "../../redux/slices";
import { selectCurrentUser } from "../../redux/store";
import SelectComponent from "../../components/selects/selectComponent";

const IndexPage: React.FC = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  // Get the auth state from Redux store
  const isAuthenticated = useSelector(
    (state: any) => state.auth.isAuthenticated
  );
  const currentUser = useSelector(selectCurrentUser);
  const imageUrl =
    currentUser?.image_file instanceof Blob
      ? URL.createObjectURL(currentUser.image_file)
      : "default-avatar.png";

  useEffect(() => {
    // Resetting user-related data when the component mounts
    if (!isAuthenticated) {
      dispatch(logOut());
    }
  }, [isAuthenticated, dispatch]);

  const handleLogin = () => {
    navigate("/auth/login");
  };

  const handleLogout = () => {
    dispatch(logOut());
  };

  const handleBudgetEntry = () => {
    // Handle start budget logic here
  };

  const handleAccount = () => {
    navigate("/account");
  };

  const handleBusinessUnitChange = (value: string | number) => {
    console.log("Selected business unit:", value);
  };

  const businessUnitOptions = [
    { value: "bu1", label: "Business Unit 1" },
    { value: "bu2", label: "Business Unit 2" },
    { value: "bu3", label: "Business Unit 3" },
  ];

  return (
    <div>
      <header
        id="navbar"
        className="overflow-hidden fixed h-fit top-0 left-0 w-full bg-gradient-to-r from-cyan-500 to-teal-700 text-white p-4 shadow-lg transform translate-y-0"
      >
        <div className="container mx-auto flex justify-between items-end">
          <div className="flex-col shadow-lg rounded-md p-2">
            <h1 className="text-2xl font-bold items-start mb-4">Budget App</h1>
            <ul className="flex items-end space-x-6 w-fit">
              <li className="transition-transform duration-300 transform hover:translate-y-1">
                <a href="#" className="hover:underline">
                  <i className="fas fa-book"></i> Tutorial
                </a>
              </li>
              <li className="transition-transform duration-300 transform hover:translate-y-1">
                <a href="#" className="hover:underline">
                  <i className="fas fa-phone"></i> Contact Support
                </a>
              </li>
              {isAuthenticated && (
                <>
                  <li className="transition-transform duration-300 transform hover:translate-y-1">
                    <a
                      href="#"
                      className="hover:underline"
                      onClick={handleLogout}
                    >
                      <i className="fas fa-sign-out-alt"></i> Logout
                    </a>
                  </li>
                  <li className="transition-transform duration-300 transform hover:translate-y-1">
                    <a
                      href="#"
                      className="hover:underline"
                      onClick={handleAccount}
                    >
                      <i className="fas fa-user-circle"></i> Account
                    </a>
                  </li>
                  {currentUser?.is_root_user && (
                    <li className="transition-transform duration-300 transform hover:translate-y-1">
                      <a href="#" className="hover:underline">
                        <i className="fas fa-chart-bar"></i> Dashboard
                      </a>
                    </li>
                  )}
                </>
              )}
            </ul>
          </div>
          <div className="flex-col">
            {isAuthenticated ? (
              <div className="flex items-end shadow-md rounded-md p-4">
                <div className="flex justify-center items-center rounded-full w-10 h-10 object-cover mr-4 border-4 border-white bg-cyan-900 text-gray-white">
                  <img
                    className="rounded-full w-full h-full object-cover text-xs"
                    src={imageUrl}
                    alt="User Image"
                    onError={(e) => {
                      const target = e.target as HTMLImageElement;
                      target.style.display = "none";
                    }}
                  />
                </div>
                <div className="flex-col">
                  <h2 className="truncate text-lg font-bold whitespace-nowrap">
                    {currentUser?.is_root_user ? (
                      <span className="text-amber-400">
                        <i className="fas fa-crown"></i> {currentUser?.username}
                      </span>
                    ) : (
                      <span className="text-emerald-400">
                        <i className="fas fa-key"></i> {currentUser?.username}
                      </span>
                    )}
                  </h2>
                  <p className="truncate break-words">{currentUser?.email}</p>
                </div>
              </div>
            ) : (
              <button
                id="loginBtn"
                className="bg-cyan-600 text-white font-semibold py-2 px-4 rounded transition duration-300 hover:bg-cyan-700 hover:shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-cyan-500"
                onClick={handleLogin}
              >
                <i className="fas fa-sign-in-alt mr-2"></i> Login
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Section */}
      <main className="mt-20 container mx-auto py-16 text-center">
        {isAuthenticated ? (
          <div className="w-fit flex flex-col justify-center mx-auto gap-3 border-2 border-stone-50 rounded-md p-4 shadow-md">
            <label htmlFor="businessUnit" className="text-2xl font-bold text-stone-500 py-2 border-b border-stone-100">Department</label>
            <SelectComponent
              id="businessUnit"
              name="businessUnit"
              options={businessUnitOptions}
              defaultValue="bu1"
              placeholder="Select Business Unit"
              onChange={handleBusinessUnitChange}
            />

            <button
              type="button"
              className="bg-cyan-500 text-white py-3 px-6 rounded-full shadow-md hover:bg-cyan-600"
              onClick={handleBudgetEntry}
            >
              <i className="fas fa-pencil-alt mr-2"></i> Start Budget
            </button>
          </div>
        ) : (
          <div>
            <h1 className="font-bold text-5xl bg-gradient-to-r from-teal-900 to-cyan-600 bg-clip-text text-transparent">
              Need an Account?
            </h1>
            <a
              href="/auth/register"
              className="text-3xl bg-gradient-to-r from-amber-300 to-amber-600 bg-clip-text text-transparent hover:animate-pulse"
            >
              Register
            </a>
          </div>
        )}
      </main>

      {/* Features Section */}
      <section className="bg-gradient-to-tr from-cyan-100 to-teal-100 to-indigo-600 py-12 rounded-md">
        <div className="container mx-auto text-center">
          <h3 className="text-3xl text-teal-800 font-semibold mb-8">
            Why Choose This?
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 p-2">
            <div className="p-6 bg-white shadow-lg rounded-lg">
              <h4 className="text-xl font-bold text-teal-700 mb-4">
                Track Expenses
              </h4>
              <p className="text-gray-700">
                Easily track and categorize your health expenses in one place.
              </p>
            </div>
            <div className="p-6 bg-white shadow-lg rounded-lg">
              <h4 className="text-xl font-bold text-teal-700 mb-4">
                Set Budget Goals
              </h4>
              <p className="text-gray-700">
                Set and monitor your budget goals to stay financially healthy.
              </p>
            </div>
            <div className="p-6 bg-white shadow-lg rounded-lg">
              <h4 className="text-xl font-bold text-teal-700 mb-4">
                Detailed Reports
              </h4>
              <p className="text-gray-700">
                Get comprehensive insights and reports for better
                decision-making.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default IndexPage;
