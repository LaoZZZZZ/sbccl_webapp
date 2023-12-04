import React, { useState } from "react";
import PasswordInput from "../common/PasswordInput.tsx";
import EmailInput from "../common/EmailInput.tsx";
import TextInput from "../common/TextInput.tsx";

interface Props {
  // login
  onSubmit: (boolean) => void;
}

const SignUp = ({ onSubmit }: Props) => {
  const [isEmailValid, setIsEmailValid] = useState("true");

  return (
    <div>
      <form className="needs-validation">
        <EmailInput parentCallback={setIsEmailValid} />
        <PasswordInput confirmPassword={true} />
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
            onSubmit(isEmailValid);
          }}
        />
      </form>
    </div>
  );
};

export default SignUp;
