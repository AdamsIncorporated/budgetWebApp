import React from 'react';
import { Link } from 'react-router-dom';
import { FaHome, FaUser, FaSignInAlt, FaUserPlus, FaKey, FaCrown } from 'react-icons/fa';

interface LinksProps {
    toggleIsOpen: () => void;
}

const Links: React.FC<LinksProps> = ({toggleIsOpen}) => (
  <ul className="flex flex-col space-y-4 text-stone-500"> 
    <li className="flex items-center hover:text-stone-800 transition ease-in duration-50" onClick={toggleIsOpen}>
      <FaHome className="mr-2" /> 
      <Link to="/">Home</Link>
    </li>
    <li className="flex items-center hover:text-stone-800 transition ease-in duration-50" onClick={toggleIsOpen}>
      <FaSignInAlt className="mr-2" /> 
      <Link to="/auth/login">Login</Link>
    </li>
    <li className="flex items-center hover:text-stone-800 transition ease-in duration-50" onClick={toggleIsOpen}>
      <FaUserPlus className="mr-2" /> 
      <Link to="/auth/register">Register</Link>
    </li>
    <li className="flex items-center hover:text-stone-800 transition ease-in duration-50" onClick={toggleIsOpen}>
      <FaUser className="mr-2" /> 
      <Link to="/auth/account">Account</Link>
    </li>
    <li className="flex items-center hover:text-stone-800 transition ease-in duration-50" onClick={toggleIsOpen}>
      <FaKey className="mr-2" /> 
      <Link to="/auth/reset-password">Reset Password</Link>
    </li>
    <li className="flex items-center hover:text-stone-800 transition ease-in duration-50" onClick={toggleIsOpen}>
      <FaCrown className="mr-2" /> 
      <Link to="/auth/register-admin/:token">Register Admin</Link>
    </li>
  </ul>
);

export default Links;