import React, { useState } from "react";
import PasswordInput from "../common/PasswordInput.tsx";
import EmailInput from "../common/EmailInput.tsx";
import Alert from "../common/Alert.tsx";

interface Props {
  // login
  onSubmit: (boolean) => void;
  // Sign up
  onSignUp: (boolean) => void;
  //Reset password
  onResetPassword: (boolean) => void;
}

const Login = ({ onSubmit, onSignUp, onResetPassword }: Props) => {
  const [isEmailValid, setIsEmailValid] = useState(false);
  const [isPasswordValid, setIsPasswordValid] = useState(false);
  return (
    <>
      <form className="needs-validation">
        <div className="mb-3 col">
          <EmailInput parentCallback={setIsEmailValid} />
          <PasswordInput
            confirmPassword={false}
            passwordValid={setIsPasswordValid}
          />
          <div className="btn-group">
            <input
              className="btn btn-primary active"
              type="button"
              value="Login"
              onClick={() => {
                onSubmit(isEmailValid && isPasswordValid);
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
    </>
  );
};

export default Login;
