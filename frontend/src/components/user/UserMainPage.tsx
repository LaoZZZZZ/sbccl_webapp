import React, { useReducer } from "react";
import AccountDetail from "./AccountDetailPage.tsx";
import Logout from "./Logout.tsx";
import Registrations from "./RegistrationsPage.tsx";
import StudentsPage from "./StudentsPage.tsx";
import UserInfo from "./UserInfo.tsx";
import { Calendar, SchoolDate } from "../common/Calendar.tsx";

interface Props {
  userInfo: UserInfo;
  logOutCallback: () => {};
}

const Page = {
  AccountDetail: 0,
  Students: 1,
  Registration: 2,
  Calendar: 3,
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
    case "go_to_calendar":
      return {
        ...state,
        page: Page.Calendar,
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
    <div>
      <nav className="navbar navbar-expand-lg navbar-light bg-light pb-3 w-100 h-10">
        <div className="container-fluid">
          <a className="navbar-brand" href="https://www.sbcclny.com">
            SBCCL
          </a>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#menubar"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="menubar">
            <ul className="navbar-nav">
              <li className="nav-item active">
                <button
                  className="btn btn-borderless"
                  onClick={() => {
                    transitionPageState({ type: "go_to_account" });
                  }}
                  id="accountPage"
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
                  id="student"
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
                  id="registration"
                >
                  Registration
                </button>
              </li>
              <li className="nav-item">
                <button
                  className="btn btn-borderless"
                  onClick={() => {
                    transitionPageState({ type: "go_to_calendar" });
                  }}
                  id="calendar"
                >
                  Calendar
                </button>
              </li>
              <li className="nav-item">
                <button
                  className="btn btn-borderless fixed-right"
                  onClick={() => {
                    Logout(userInfo, logOutCallback);
                  }}
                  id="logout"
                >
                  Logout
                </button>
              </li>
            </ul>
          </div>
        </div>
      </nav>
      {state?.page === Page.AccountDetail && (
        <div className="pt-3 w-75 mx-auto">
          <AccountDetail userInfo={userInfo} />
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
      {state?.page === Page.Calendar && (
        <div className="pt-3 w-75 mx-auto">
          <Calendar
            schoolDates={[
              {
                event: "Dragon Boat Festival",
                date: new Date("Sep 14, 2024"),
                school_year_start: new Date("Sep 14, 2024"),
                school_year_end: new Date("Jun 14, 2025"),
              },
              {
                event: "School start day",
                date: new Date("Sep 07, 2024"),
                school_year_start: new Date("Sep 07, 2024"),
                school_year_end: new Date("Jun 07, 2025"),
              },
              {
                event: "Last school date",
                date: new Date("Jun 07, 2025"),
                school_year_start: new Date("Sep 07, 2024"),
                school_year_end: new Date("Jun 07, 2025"),
              },
              {
                event: "Last school date",
                date: new Date("Mar 07, 2024"),
                school_year_start: new Date("Sep 07, 2024"),
                school_year_end: new Date("Jun 07, 2025"),
              },
              {
                event: "Dragon Boat Festival",
                date: new Date("Feb 14, 2024"),
                school_year_start: new Date("Sep 14, 2024"),
                school_year_end: new Date("Jun 14, 2025"),
              },
            ]}
          />
        </div>
      )}
    </div>
  );
};

export default UserMainPage;
