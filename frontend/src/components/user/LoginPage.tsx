import React, { useState } from "react";
import PasswordInput from "../common/PasswordInput.tsx";
import EmailInput from "../common/EmailInput.tsx";
import axios from "axios";
import Alert from "../common/Alert.tsx";
import UserInfo from "./UserInfo.tsx";

interface Props {
  onLoginSuccess: () => void;
  onSignUp: () => void;
  onResetPassword: () => void;
}

const LoginPage = ({ onLoginSuccess, onSignUp, onResetPassword }: Props) => {
  const [emailAddress, setEmailAddress] = useState("");
  const [password, setPassword] = useState("");
  const [loginFailed, setLoginFailed] = useState(false);
  const [loginErrorMsg, setLoginErrorMsg] = useState("");
  return (
    <div className="w-50 form-control mx-auto align-middle">
      <form className="control-form">
        <EmailInput parentCallback={setEmailAddress} />
        <PasswordInput
          // No need to let the user to confirm their password separately.
          confirmPassword={false}
          retrievePassword={setPassword}
        />
        <div className="btn-group">
          <input
            className="btn btn-primary active"
            type="button"
            value="Login"
            onClick={async () => {
              if (emailAddress === "" || password === "") {
                setLoginErrorMsg("Please provide valid email or password!");
                setLoginFailed(true);
                return;
              }
              await axios
                .put(
                  process.env.REACT_APP_BE_URL_PREFIX +
                    "/rest_api/members/login/",
                  {},
                  {
                    auth: {
                      username: emailAddress,
                      password: password,
                    },
                  }
                )
                .then(function (response) {
                  if (response.status === 202) {
                    const user_data = response.data;
                    const user_info: UserInfo = {
                      auth: {
                        password: password,
                        username: user_data.user.username,
                      },
                      user: user_data.user,
                    };
                    onLoginSuccess(user_info);
                  }
                })
                .catch(function (error) {
                  if (error.response.data) {
                    setLoginErrorMsg(error.response.data);
                  } else {
                    setLoginErrorMsg("Unexpected error!");
                  }
                  setLoginFailed(true);
                });
            }}
          />
          <input
            className="btn btn-primary"
            type="button"
            value="Sign up"
            onClick={() => {
              onSignUp();
            }}
          />
          <input
            className="btn btn-secondary"
            type="button"
            value="Reset password"
            onClick={() => {
              onResetPassword();
            }}
          />
        </div>
      </form>
      {loginFailed && (
        <div>
          <Alert
            success={false}
            message={loginErrorMsg}
            parentCallback={() => {
              setLoginErrorMsg("");
              setLoginFailed(false);
            }}
          />
        </div>
      )}
    </div>
  );
};

export default LoginPage;
