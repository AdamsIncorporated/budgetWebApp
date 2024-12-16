import React from "react";
import { useSelector, useDispatch } from "react-redux";
import { RootState } from "../../stores/store";

function AccountBar() {
  const isAuthenticated = useSelector(
    (state: RootState) => state.auth.isAuthenticated
  );

  return (
    isAuthenticated && (
      <div className="rounded-md shadow-md bg-inherit text-white">
        <div>ACCOUNT BAR</div>
      </div>
    )
  );
}

export default AccountBar;
