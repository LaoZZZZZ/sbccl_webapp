import LoginPage from "../user/LoginPage.tsx";
import SignUpPage from "../user/SignUpPage.tsx";
import ResetPasswordPage from "../user/ResetPasswordPage.tsx";
import React, { useReducer } from "react";

interface Props {
  loginSuccessCallback: ({}) => {};
}

const Page = {
  StartLogin: 0, // User is on login page
  StartResetPassword: 1, // User is on reset password page
  StartSignUp: 2, // user is on the sign up page
};

const reducer = (userState, action) => {
  switch (action.type) {
    case "login":
      return {
        ...userState,
        page: Page.StartLogin,
        user_info: action.user_info,
      };
    case "signup":
      return {
        ...userState,
        page: Page.StartSignUp,
        user_info: action.user_info,
      };
    case "reset_password":
      return {
        ...userState,
        page: Page.StartResetPassword,
        user_info: action.user_info,
      };
    default:
      throw new Error("Unrecognized action type?");
  }
};

const INITIAL_STATE = {
  /* Default on login page*/
  page: Page.StartLogin,
  // Basic user information including
  // a. username, password
  // b. Auth token
  user_info: null,
};

// User front page before user login. It includes the following workflow
// 1. User login with known username and passworld
// 2. new user sign up
// 3. Reset password if the user forgets their password.
const UserFrontPage = ({ loginSuccessCallback }: Props) => {
  const [userState, dispatch] = useReducer(reducer, INITIAL_STATE);

  return (
    <div className="container-xxl">
      {userState.page === Page.StartLogin && (
        <LoginPage
          onLoginSuccess={(user_info) => {
            loginSuccessCallback(user_info);
          }}
          onSignUp={() => {
            dispatch({ type: "signup" });
          }}
          onResetPassword={() => {
            dispatch({ type: "reset_password" });
          }}
        />
      )}

      {userState.page === Page.StartSignUp && (
        <SignUpPage
          onBackToLogin={() => {
            dispatch({ type: "login" });
          }}
        />
      )}

      {userState.page === Page.StartResetPassword && (
        <ResetPasswordPage
          onBackToLogin={() => {
            dispatch({ type: "login" });
          }}
        />
      )}
    </div>
  );
};

export default UserFrontPage;
