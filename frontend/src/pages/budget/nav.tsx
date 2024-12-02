import React from "react";
import { FaArrowLeft, FaCrown, FaKey, FaSave, FaServer } from "react-icons/fa";

interface NavProps {
  fiscalYear: string;
  businessUnitId: string;
  currentUser: {
    isAuthenticated: boolean;
    isRootUser: boolean;
    username: string;
    email: string;
    profileImageBase64?: string;
  };
  historicalFiscalYearPicklist: JSX.Element;
  proposedFiscalYearPicklist: JSX.Element;
  businessUnitPicklist: JSX.Element;
}

const Nav: React.FC<NavProps> = ({
  fiscalYear,
  businessUnitId,
  currentUser,
  historicalFiscalYearPicklist,
  proposedFiscalYearPicklist,
  businessUnitPicklist,
}) => {
  return (
    <nav>
      <div className="mb-3 flex justify-between border-b-2 border-stone-100 py-3 items-end">
        <div className="flex-col">
          <a className="hover:underline text-teal-700" href="/">
            <FaArrowLeft className="inline" /> Home
          </a>
          <h1 className="text-stone-300">
            {fiscalYear} for Business Unit ID {businessUnitId}
          </h1>
        </div>
        <div className="flex-col">
          {currentUser.isAuthenticated && (
            <div className="flex items-end shadow-md rounded-md p-4">
              <div className="flex justify-center items-center rounded-full w-10 h-10 object-cover mr-4 border-4 border-stone-300 bg-cyan-900 text-gray-white">
                {currentUser.profileImageBase64 ? (
                  <img
                    className="rounded-full w-full h-full object-cover text-xs"
                    src={`data:image/jpeg;base64,${currentUser.profileImageBase64}`}
                    alt="User Image"
                    onError={(e) => {
                      const target = e.currentTarget;
                      target.style.display = "none";
                      target.parentElement!.style.fontSize = "8px";
                      target.parentElement!.textContent = "User";
                    }}
                  />
                ) : (
                  "User"
                )}
              </div>
              <div className="flex-col">
                <h2 className="truncate text-xs font-bold whitespace-nowrap">
                  {currentUser.isRootUser ? (
                    <span className="text-amber-400">
                      <FaCrown className="inline" /> {currentUser.username}
                    </span>
                  ) : (
                    <span className="text-emerald-400">
                      <FaKey className="inline" /> {currentUser.username}
                    </span>
                  )}
                </h2>
                <p className="truncate break-words text-xs text-stone-300">
                  {currentUser.email}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
      <div className="overflow-auto flex flex-row justify-between items-end px-2 my-5 pb-2 gap-2">
        <div className="flex flex-row items-end gap-3">
          <div className="flex flex-col text-teal-700">
            <div className="p-2 text-xs text-nowrap">Historical Fiscal Year</div>
            {historicalFiscalYearPicklist}
          </div>
          <div className="flex flex-col text-teal-700">
            <div className="p-2 text-xs text-nowrap">Proposed Fiscal Year</div>
            {proposedFiscalYearPicklist}
          </div>
          <div className="flex flex-col text-teal-700">
            <div className="p-2 text-xs text-nowrap">Department</div>
            {businessUnitPicklist}
          </div>
        </div>
        <div className="flex flex-col justify-between gap-4">
          <div className="flex flex-row">
            <button
              id="queryBtn"
              type="button"
              className="flex items-center justify-center bg-cyan-500 text-white font-bold py-2 px-4 rounded hover:bg-cyan-600 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:ring-opacity-75 mr-4"
            >
              <FaServer className="mr-2" />
              Query
            </button>
            <button
              form="budgetsForm"
              type="submit"
              className="flex items-center justify-center bg-teal-500 text-white font-bold py-2 px-4 rounded hover:bg-teal-600 focus:outline-none focus:ring-2 focus:ring-teal-400 focus:ring-opacity-75"
            >
              <FaSave className="mr-2" />
              Save
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Nav;
