import React, { useReducer } from "react";
import AccountDetail from "./AccountDetailPage.tsx";
import Logout from "./Logout.tsx";
import Registrations from "./RegistrationsPage.tsx";
import StudentsPage from "./StudentsPage.tsx";
import UserInfo from "./UserInfo.tsx";

interface Props {
  userInfo: UserInfo;
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
  const INITIAL_PAGE = {
    /* Default on account detail page*/
    page: Page.AccountDetail,
  };
  const [state, transitionPageState] = useReducer(SwitchPage, INITIAL_PAGE);
  return (
    <>
      <div className="navbar navbar-expand-lg bg-light navbar-toggler pb-3 w-100 h-10">
        <a className="navbar-brand" href="https://www.sbcclny.com">
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
                Registration
              </button>
            </li>
            <li className="nav-item ">
              <button
                className="btn btn-borderless"
                onClick={() => {
                  Logout(userInfo, logOutCallback);
                }}
              >
                Logout
              </button>
            </li>
          </ul>
        </div>
      </div>
      {state?.page === Page.AccountDetail && (
        <div className="pt-3 w-75 mx-auto">
          <AccountDetail userInfo={userInfo.user} />
        </div>
      )}
      {state?.page === Page.Students && (
        <div className="pt-3 w-75 mx-auto">
          <StudentsPage userInfo={userInfo} />
        </div>
      )}
      {state?.page === Page.Registration && (
        <div className="pt-3 w-75 mx-auto">
          <Registrations userInfo={userInfo} />
        </div>
      )}
    </>
  );
};

export default UserMainPage;
