import React, { useContext, useState } from "react";
import PasswordInput from "../common/PasswordInput.tsx";
import EmailInput from "../common/EmailInput.tsx";
import axios from "axios";

import { UserContext } from "../app/App.tsx";
import Alert from "../common/Alert.tsx";

const UserActions = {
  Login: 0, // User is attempting to login with entered cridential.
  SignUp: 1, // User is attempting to sign up with entered information
  ResetPassword: 2, // User is attempting to reset password with new password.
  Logout: 3, // User is attempting to logout.
};

const LoginPage = ({ onSignUp, onResetPassword }: Props) => {
  const [emailAddress, setEmailAddress] = useState("");
  const [password, setPassword] = useState("");
  const [loginFailed, setLoginFailed] = useState(false);

  const [, dispatch] = useContext(UserContext);

  return (
    <>
      <form className="needs-validation">
        <div className="mb-3 col">
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
                console.log("login" + emailAddress + ":" + password);
                if (emailAddress === "" || password === "") {
                  setLoginFailed(true);
                  return;
                }
                console.log("sending login request");
                await axios
                  .put(
                    "http://localhost:8000/rest_api/members/login/",
                    {},
                    {
                      auth: {
                        username: emailAddress,
                        password: password,
                      },
                    }
                  )
                  .then(function (response) {
                    if (response.status == 202) {
                      const user_info = response.data;
                      dispatch({ type: 0, user_info });
                    }
                  })
                  .catch(function (error) {
                    setLoginFailed(true);
                  });
              }}
            />
            <input
              className="btn btn-primary"
              type="button"
              value="Sign up"
              onClick={() => {
                onSignUp(true);
              }}
            />
            <input
              className="btn btn-secondary"
              type="button"
              value="Reset password"
              onClick={() => {
                onResetPassword(true);
              }}
            />
          </div>
        </div>
      </form>
      {loginFailed && (
        <Alert
          message="Invalid user or password is provided!"
          parentCallback={() => {
            setLoginFailed(false);
          }}
        />
      )}
    </>
  );
};

export default LoginPage;
