import React, { useContext, useState } from "react";
import PasswordInput from "../common/PasswordInput.tsx";
import EmailInput from "../common/EmailInput.tsx";
import axios from "axios";
import { UserContext } from "../app/App.tsx";
import Alert from "../common/Alert.tsx";

interface Props {
  onLoginSuccess: ({}) => void;
  onSignUp: () => void;
  onResetPassword: () => void;
}

const LoginPage = ({ onLoginSuccess, onSignUp, onResetPassword }: Props) => {
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
                if (emailAddress === "" || password === "") {
                  setLoginFailed(true);
                  return;
                }
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
                      onLoginSuccess(user_info);
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
        </div>
      </form>
      {loginFailed && (
        <Alert
          success={false}
          message="Invalid username or password is provided!"
          parentCallback={() => {
            setLoginFailed(false);
          }}
        />
      )}
    </>
  );
};

export default LoginPage;