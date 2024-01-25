import React, { useEffect, useState } from "react";
import PageHead from "../common/PageHead.tsx";
import ListStudent from "./ListStudent.tsx";

interface Props {
  userInfo: React.ReactNode;
}

// Main page for user profile after login.
// Contains the following components:
// 1. User profile
// 2. Students under this user
// 3. Registrations associated with each student
const UserMainPage = ({ userInfo }: Props) => {
  return (
    <>
      <div className="navbar navbar-expand-lg bg-light navbar-toggler pb-3 w-100 h-10">
        <a className="navbar-brand" href="#">
          SBCCL
        </a>
        <button
          className="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarSupportedContent">
          <ul className="navbar-nav mr-auto">
            <li className="nav-item active">
              <button className="btn btn-borderless">Account Profile</button>
            </li>
            <li className="nav-item">
              <button className="btn btn-borderless">Students</button>
            </li>
            <li className="nav-item">
              <button className="btn btn-borderless">Register class</button>
            </li>
            <li className="nav-item">
              <button className="btn btn-borderless">Logout</button>
            </li>
          </ul>
        </div>
      </div>
      <div className="pt-3 w-75 mx-auto">
        <ListStudent userInfo={userInfo} />
      </div>
    </>
  );
};

export default UserMainPage;
