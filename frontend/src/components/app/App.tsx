import React, {
  Children,
  Component,
  useEffect,
  useReducer,
  useState,
} from "react";

import LoginPage from "../user/LoginPage.tsx";
import Details from "../user/Details.tsx";
import SignUp from "../user/SignUp.tsx";
import ResetPassword from "../user/ResetPassword.tsx";
import axios from "axios";
import Alert from "../common/Alert.tsx";
// Some Hardcoded user information for development purpose. Read data will be loaded from the
// backend.
const usersList = [
  {
    email: "luzhao1986@gmail.com",
    first_name: "Lu",
    last_name: "Zhao",
    joined_date: "2023-11-01",
    id: 2,
    sign_up_status: "V",
  },
];

const Page = {
  StartLogin: 0, // User is on login page
  StartResetPassword: 2, // User is on reset password page
  StartSignUp: 3, // user is on the sign up page
  PostLogin: 4, // User successfully logged in, showing the user profile page.
};

const UserActions = {
  Login: 0, // User is attempting to login with entered cridential.
  SignUp: 1, // User is attempting to sign up with entered information
  ResetPassword: 2, // User is attempting to reset password with new password.
  Logout: 3, // User is attempting to logout.
};

const userLogout = async (user_state) => {
  await axios
    .put("http://localhost:8000/rest_api/members/logout", {
      user_state,
    })
    .then(function (response) {
      console.log(response);
      return {
        page: Page.StartLogin,
      };
    });
};

const userSignUp = async (user_profile) => {
  const userLoginResponse = await axios
    .put("http://localhost:8000/rest_api/members/sign-up", {
      user_profile,
    })
    .then(function (response) {
      console.log(response);
      if (response.status == 200) {
        return {
          page: Page.StartLogin,
          // Add students here.
        };
      } else {
        return {
          page: Page.StartSignUp,
          // Add students here.
        };
      }
    });
};

const userResetPassword = async (user_state) => {
  const userLoginResponse = await axios
    .put("http://localhost:8000/rest_api/members/reset-password", {
      user_state,
    })
    .then(function (response) {
      console.log(response);
      if (response.status == 200) {
        return {
          page: Page.PostLogin,
          // Add students here.
        };
      } else {
        return {
          page: Page.StartResetPassword,
          // Add students here.
        };
      }
    });
};

const reducer = (user_repo, action) => {
  switch (action.type) {
    case UserActions.Login:
      console.log(user_repo.user_info);
      return { ...user_repo, page: Page.PostLogin };
    case UserActions.Logout:
      return {
        page: Page.StartLogin,
        user_info: null,
      };
    case UserActions.SignUp:
      return {
        page: Page.StartSignUp,
        user_info: null,
      };
    case UserActions.ResetPassword:
      return {
        page: Page.StartResetPassword,
        user_info: null,
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
  student: [],
};

export const UserContext = React.createContext([]);

const App = () => {
  const [user_repo, dispatch] = useReducer(reducer, INITIAL_STATE);

  return (
    <UserContext.Provider value={[user_repo, dispatch]}>
      <div className="container-sm">
        {user_repo.page === Page.StartLogin && (
          <LoginPage
            onSubmit={(loginReady) => {
              console.log("submitting");
              if (loginReady) {
                dispatch({ type: UserActions.Login });
              }
            }}
            onSignUp={() => {
              dispatch({ type: UserActions.SignUp });
            }}
            onResetPassword={() => {
              dispatch({ type: UserActions.ResetPassword });
            }}
          />
        )}

        {user_repo.page === Page.PostLogin && <Details />}

        {user_repo.page === Page.StartSignUp && (
          <SignUp
            onSubmit={(signupReady) => {
              if (signupReady) {
                dispatch({ type: UserActions.Login });
              }
            }}
            onBackToLogin={() => {
              dispatch({ type: UserActions.Login });
            }}
          />
        )}

        {user_repo.page === Page.StartResetPassword && (
          <ResetPassword
            onReset={(resetSuccess) => {
              if (resetSuccess) {
                dispatch({ type: UserActions.Login });
              }
            }}
            onBackToLogin={() => {
              dispatch({ type: UserActions.Login });
            }}
          />
        )}
        {/* { 
      {user_repo.user_state === UserStates.LoginFailure && (
        <Alert
          message="Invalid user credential is provided"
          parentCallback={() => {
            console.log("login failed");
            dispatch({ type: Action.StartLogin });
          }}
        /> }
        
      )} */}
      </div>
    </UserContext.Provider>
  );
};

export default App;
