import React, { useState } from "react";
import { FaHome, FaUser, FaCog } from "react-icons/fa";
import { useDispatch } from "react-redux";
import NavbarComponent from "../navbar/navbarComponent";

export interface SidebarItem {
  name: string;
  icon: JSX.Element;
  route: string;
}

const sidebarItems: SidebarItem[] = [
  { name: "Home", icon: <FaHome />, route: "/" },
  { name: "Profile", icon: <FaUser />, route: "/profile" },
  { name: "Settings", icon: <FaCog />, route: "/settings" },
];

const SidebarComponent: React.FC = () => {
  const dispatch = useDispatch();

  const handleAccount = () => {
    
  };

  const [isExpanded, setIsExpanded] = useState(false);

  const toggleSidebar = () => {
    setIsExpanded(!isExpanded);
  };

  const toggleIcon = isExpanded ? (
    <svg
      className="w-6 h-6 transform rotate-180 transition duration-200 ease-in-out"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="2"
        d="M6 18L18 6M6 6l12 12"
      />
    </svg>
  ) : (
    <svg
      className="w-6 h-6 transition duration-200 ease-in-out"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="2"
        d="M4 6h16M4 12h16M4 18h16"
      />
    </svg>
  );

  return (
    <div className="relative"> {/* Wrap header and content in a relative container */}
      <button
        type="button"
        className="bg-inherit shadow-md rounded-md p-4 focus:outline-none absolute left-0 top-0 z-50"
        onClick={toggleSidebar}
      >
        {toggleIcon}
      </button>
      <div
        className={`absolute z-40 h-screen overflow-auto bg-black text-cyan-500 transition duration-200 ease-in-out transform ${
          isExpanded ? "top-0 left-0" : "-translate-x-full"
        }`}
      >
        <nav className="flex flex-col pt-6 px-6">
          {sidebarItems.map((item) => (
            <a
              key={item.name}
              href={item.route}
              className="flex items-center mb-6 hover:text-gray-200" // Tailwind classes for styling
            >
              {item.icon}
              <span className="ml-4 text-lg">{item.name}</span>
            </a>
          ))}
        </nav>
      </div>
      <div
        className={`flex-grow px-4 pt-4 pb-16 transition duration-200 ease-in-out transform ${
          isExpanded ? "ml-64" : "ml-0"
        }`}
      >
        <NavbarComponent/>
      </div>
    </div>
  );
};

export default SidebarComponent;