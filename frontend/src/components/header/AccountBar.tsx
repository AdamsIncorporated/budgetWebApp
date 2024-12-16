import React from "react";
import { useSelector } from "react-redux";
import {
  selectIsAuthenticated,
  selectCurrentUser,
} from "../../stores/slices/authSlice";
import { FaCrown } from "react-icons/fa";
import { Link } from "react-router-dom";

function AccountBar() {
  const isAuthenticated = useSelector(selectIsAuthenticated);
  const currentUser = useSelector(selectCurrentUser);

  return (
    isAuthenticated && (
      <div className="rounded-md shadow-md bg-inherit text-white text-xs p-2">
        <div className="flex justify-start items-center gap-4 border-b pb-1">
          {currentUser?.is_root_user && <FaCrown className="text-amber-500" />}
          <div className="font-bold hover:underline">
            <Link to="/auth/account">{currentUser?.username} </Link>
          </div>
        </div>
        <div>{`${currentUser?.first_name} ${currentUser?.last_name}`}</div>
      </div>
    )
  );
}

export default AccountBar;
