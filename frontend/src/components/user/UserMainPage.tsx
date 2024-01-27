import React, { useContext, useReducer } from "react";
import ListStudent from "./ListStudent.tsx";
import AccountDetail from "./AccountDetailPage.tsx";
import Registration from "./RegistrationPage.tsx";
import { UserContext } from "../app/App.tsx";
import axios from "axios";

interface Props {
  userInfo: React.ReactNode;
  logOutCallback: () => {};
}

const Page = {
  AccountDetail: 0,
  Students: 1,
  Registration: 2,
};

const SwitchPage = (state, action) => {
  switch (action.type) {
    case "go_to_students":
      return {
        ...state,
        page: Page.Students,
      };
    case "go_to_registration":
      return {
        ...state,
        page: Page.Registration,
      };
    case "go_to_account":
      return {
        ...state,
        page: Page.AccountDetail,
      };
  }
};

// Main page for user profile after login.
// Contains the following components:
// 1. User profile
// 2. Students under this user
// 3. Registrations associated with each student
const UserMainPage = ({ userInfo, logOutCallback }: Props) => {
  const logOut = async (userInfo) => {
    await axios
      .put(
        "http://localhost:8000/rest_api/members/logout/",
        {},
        {
          auth: userInfo.auth,
        }
      )
      .then(function (response) {
        if (response.status == 202) {
          logOutCallback();
        }
      })
      .catch(function (error) {
        logOutCallback();
      });
  };
  const INITIAL_PAGE = {
    /* Default on account detail page*/
    page: Page.AccountDetail,
  };
  const [state, transitionPageState] = useReducer(SwitchPage, INITIAL_PAGE);
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
              <button
                className="btn btn-borderless"
                onClick={() => {
                  transitionPageState({ type: "go_to_account" });
                }}
              >
                Account Profile
              </button>
            </li>
            <li className="nav-item">
              <button
                className="btn btn-borderless"
                onClick={() => {
                  transitionPageState({ type: "go_to_students" });
                }}
              >
                Students
              </button>
            </li>
            <li className="nav-item">
              <button
                className="btn btn-borderless"
                onClick={() => {
                  transitionPageState({ type: "go_to_registration" });
                }}
              >
                Register class
              </button>
            </li>
            <li className="nav-item">
              <button
                className="btn btn-borderless"
                onClick={() => {
                  logOut(userInfo);
                }}
              >
                Logout
              </button>
            </li>
          </ul>
        </div>
      </div>
      {state?.page == Page.AccountDetail && (
        <div className="pt-3 w-75 mx-auto">
          <AccountDetail userInfo={userInfo.user} />
        </div>
      )}
      {state?.page == Page.Students && (
        <div className="pt-3 w-75 mx-auto">
          <ListStudent userInfo={userInfo} />
        </div>
      )}
      {state?.page == Page.Registration && (
        <div className="pt-3 w-75 mx-auto">
          <Registration userInfo={userInfo} />
        </div>
      )}
    </>
  );
};

export default UserMainPage;
