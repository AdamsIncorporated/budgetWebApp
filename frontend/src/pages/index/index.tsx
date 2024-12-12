import React from 'react';
import { Outlet } from 'react-router-dom';

const IndexPage = () => {
  return (
    <div>
      <Outlet />
    </div>
  );
};

export default IndexPage;