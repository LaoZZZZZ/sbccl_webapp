import React, { Children, Component, useState } from "react";
import Login from "../user/Login.tsx";
import PasswordInput from "../common/PasswordInput.tsx";
import Details from "../user/Details.tsx";
import SignUp from "../user/SignUp.tsx";
import ResetPassword from "../user/ResetPassword.tsx";
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
  StartLogin: 0,
  StartSignUp: 1,
  LoginSuccess: 2,
  StartResetPassword: 3,
};

const App = () => {
  /* Default on login page*/
  const [userState, setUserState] = useState(UserStates.StartLogin);

  return (
    <div className="container-sm">
      {userState === UserStates.StartLogin && (
        <Login
          onSubmit={(loginReady) => {
            setUserState(UserStates.LoginSuccess);
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
    </div>
  );
};

export default App;
