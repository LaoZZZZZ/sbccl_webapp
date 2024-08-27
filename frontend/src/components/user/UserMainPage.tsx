import React, { useReducer } from "react";
import AccountDetail from "./AccountDetailPage.tsx";
import Logout from "./Logout.tsx";
import Registrations from "./RegistrationsPage.tsx";
import StudentsPage from "./StudentsPage.tsx";
import { AccountInfo } from "./UserInfo.tsx";
import CalendarDetailPage from "./CalendarDetailPage.tsx";
import CoursesNavigationPage from "./CoursesNavigationPage.tsx";
import Terms from "../common/Terms.tsx";

// Parent needs to sign the terms every year before Aug 24th.
const needToSignTerms = (userInfo: AccountInfo) => {
  // Board member does not need to sign the form.
  if (userInfo.user.member_type === "B") {
    return false;
  }
  if (userInfo.user.term_signed_date == null) {
    return true;
  }

  const previousSignDate = new Date(userInfo.user.term_signed_date);
  let nextSignYear = new Date("Aug 24th, 2024 23:59:59");
  nextSignYear.setFullYear(new Date().getFullYear());
  if (process.env.REACT_APP_COURSE_EXCHANGE_CUTOFF_DATE !== null) {
    nextSignYear = new Date(process.env.REACT_APP_COURSE_EXCHANGE_CUTOFF_DATE);
  }
  return (
    Math.round(
      (nextSignYear.getTime() - previousSignDate.getTime()) / (1000 * 3600 * 24)
    ) >= 365
  );
};

interface Props {
  userInfo: AccountInfo;
  logOutCallback: () => {};
}

const Page = {
  AccountDetail: 0,
  Students: 1,
  Registration: 2,
  Calendar: 3,
  Rosters: 4,
  // If the user has not signed the terms for this year, direct the user to the term
  // sign page.
  Terms: 5,
};

const SwitchPage = (state, action) => {
  switch (action.type) {
    case "go_to_terms":
      return {
        ...state,
        page: Page.Terms,
      };
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
    case "go_to_rosters":
      return {
        ...state,
        page: Page.Rosters,
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
    page: needToSignTerms(userInfo) ? Page.Terms : Page.AccountDetail,
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
                    if (needToSignTerms(userInfo)) {
                      transitionPageState({ type: "go_to_terms" });
                    } else {
                      transitionPageState({ type: "go_to_account" });
                    }
                  }}
                  id="accountPage"
                >
                  Account Profile
                </button>
              </li>
              {userInfo.user.member_type === "Parent" && (
                <li className="nav-item">
                  <button
                    className="btn btn-borderless"
                    onClick={() => {
                      if (needToSignTerms(userInfo)) {
                        transitionPageState({ type: "go_to_terms" });
                      } else {
                        transitionPageState({ type: "go_to_students" });
                      }
                    }}
                    id="student"
                  >
                    Students
                  </button>
                </li>
              )}
              {userInfo.user.member_type === "Parent" && (
                <li className="nav-item">
                  <button
                    className="btn btn-borderless"
                    onClick={() => {
                      if (needToSignTerms(userInfo)) {
                        transitionPageState({ type: "go_to_terms" });
                      } else {
                        transitionPageState({ type: "go_to_registration" });
                      }
                    }}
                    id="registration"
                  >
                    Registration
                  </button>
                </li>
              )}
              <li className="nav-item">
                <button
                  className="btn btn-borderless"
                  onClick={() => {
                    if (needToSignTerms(userInfo)) {
                      transitionPageState({ type: "go_to_terms" });
                    } else {
                      transitionPageState({ type: "go_to_calendar" });
                    }
                  }}
                  id="calendar"
                >
                  Calendar
                </button>
              </li>
              {userInfo.user.member_type !== "Parent" && (
                <li className="nav-item">
                  <button
                    className="btn btn-borderless"
                    onClick={() => {
                      transitionPageState({ type: "go_to_rosters" });
                    }}
                    id="calendar"
                  >
                    Rosters
                  </button>
                </li>
              )}
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
          <CalendarDetailPage userAuth={userInfo.auth} />
        </div>
      )}
      {state?.page === Page.Rosters && (
        <div className="pt-3 w-75 mx-auto">
          <CoursesNavigationPage userAuth={userInfo.auth} />
        </div>
      )}
      {state?.page === Page.Terms && (
        <div className="pt-3 w-75 mx-auto">
          <Terms
            userInfo={userInfo}
            callback={() => {
              // Term is signed successfully.
              userInfo.user.term_signed_date = new Date();
              transitionPageState({ type: "go_to_account" });
            }}
            // Logout the user if
            failureCallback={function () {
              Logout(userInfo, logOutCallback);
            }}
          />
        </div>
      )}
    </div>
  );
};

export default UserMainPage;
