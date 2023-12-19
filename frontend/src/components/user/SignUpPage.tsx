import React, { useState } from "react";
import PasswordInput from "../common/PasswordInput.tsx";
import EmailInput from "../common/EmailInput.tsx";
import TextInput from "../common/TextInput.tsx";

interface Props {
  // login
  onSubmit: (boolean) => void;
  onBackToLogin: () => void;
}

const SignUpPage = ({ onSubmit, onBackToLogin }: Props) => {
  const [isEmailValid, setIsEmailValid] = useState(false);
  const [isPasswordValid, setIsPasswordValid] = useState(false);
  return (
    <div>
      <form className="needs-validation">
        <EmailInput parentCallback={setIsEmailValid} />
        <PasswordInput
          confirmPassword={true}
          passwordValid={setIsPasswordValid}
        />
        <TextInput
          labelText="First name"
          inputType={"text"}
          requiredInput={true}
        />
        <TextInput
          labelText="Last name"
          inputType={"text"}
          requiredInput={true}
        />
        <TextInput
          labelText="Cell phone"
          inputType={"tel"}
          requiredInput={false}
        />
        <input
          className="btn btn-primary active"
          type="button"
          value="Sign up"
          onClick={() => {
            if (isEmailValid && isPasswordValid) {
              onSubmit(true);
            }
          }}
        />
        <input
          className="btn btn-secondary"
          type="button"
          value="Back to login"
          onClick={() => {
            onBackToLogin();
          }}
        />
      </form>
    </div>
  );
};

export default SignUpPage;
