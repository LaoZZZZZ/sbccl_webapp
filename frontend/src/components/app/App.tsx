import React, { Children, Component, useEffect, useState } from "react";
import Login from "../user/Login.tsx";
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

const UserStates = {
  StartLogin: 0, // initial state
  StartSignUp: 1, // User wants to sign up, switch to sign up page
  StartResetPassword: 2, // user wants to reset password, render password reset page
  LoginReady: 3, // User entered valid credentials, ready to send login request to backend.
  LoginSuccess: 4, // Login succeeded, render user information.
  LoginFailure: 5, // Login failed, report error and transition back to login page (StartLogin)
};

const App = () => {
  /* Default on login page*/
  const [userState, setUserState] = useState(UserStates.StartLogin);
  const [userData, setUserData] = useState(null);
  const userLogin = async () => {
    try {
      const userLoginResponse = await axios.get(
        "http://localhost:8000/rest_api/user"
      );
      console.log(userLoginResponse.statusText);
      if (userLoginResponse.status == 200) {
        setUserState(UserStates.LoginSuccess);
        setUserData(userLoginResponse.data);
      } else {
        setUserState(UserStates.LoginFailure);
      }
    } catch (e) {}
  };

  useEffect(() => {
    if (userState !== UserStates.LoginReady) {
      return;
    }
    userLogin();
  }, [userState, userData]);

  return (
    <div className="container-sm">
      {userState === UserStates.StartLogin && (
        <Login
          onSubmit={(loginReady) => {
            console.log("submitting");
            if (loginReady) {
              setUserState(UserStates.LoginReady);
            } else {
              console.log("failed to login");
              setUserState(UserStates.LoginFailure);
            }
          }}
          onSignUp={() => {
            setUserState(UserStates.StartSignUp);
          }}
          onResetPassword={() => {
            setUserState(UserStates.StartResetPassword);
          }}
        />
      )}

      {userState === UserStates.LoginSuccess && <Details />}

      {userState === UserStates.StartSignUp && (
        <SignUp
          onSubmit={(signupReady) => {
            if (signupReady) {
              setUserState(UserStates.StartLogin);
            }
          }}
        />
      )}

      {userState === UserStates.StartResetPassword && (
        <ResetPassword
          onReset={(resetSuccess) => {
            if (resetSuccess) {
              setUserState(UserStates.StartLogin);
            }
          }}
        />
      )}

      {userState === UserStates.LoginFailure && (
        <Alert
          message="Invalid user credential is provided"
          parentCallback={() => {
            console.log("login failed");
            setUserState(UserStates.StartLogin);
          }}
        />
      )}
    </div>
  );
};

export default App;
