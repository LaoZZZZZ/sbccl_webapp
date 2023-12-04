import React, { useState } from "react";
import validator from "validator";

interface ConformPasswordProps {
  passwordInput: string;
  showPassword: boolean;
}

const PasswordConfirmation = ({
  passwordInput,
  showPassword,
}: ConformPasswordProps) => {
  const [errorMessage, setErrorMessage] = useState("");
  const matchPassword = (passwordInput, confirmedPassword) => {
    if (passwordInput !== confirmedPassword) {
      setErrorMessage("Mismatched password!");
    } else {
      setErrorMessage("");
    }
  };

  return (
    <>
      <label htmlFor="passwordConfirm" className="form-label">
        Confirm password
      </label>
      <input
        type={showPassword ? "text" : "password"}
        className="form-control"
        id="passwordConfirm"
        onChange={(e) => {
          matchPassword(passwordInput, e.target.value);
        }}
      />
      {errorMessage === "" ? null : (
        <div
          id="passwordHelpBlock"
          className={errorMessage === "" ? "form-text" : "text-warning"}
        >
          {errorMessage}
        </div>
      )}
    </>
  );
};

interface Props {
  // If true, add another input for password verification.
  confirmPassword: boolean;
}

const PasswordInput = ({ confirmPassword }: Props) => {
  const [errorMessage, setErrorMessage] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const validate = (password) => {
    if (
      validator.isStrongPassword(password, {
        minLength: 8,
        minNumbers: 1,
        minLowercase: 1,
        minUppercase: 1,
      })
    ) {
      setErrorMessage("");
    } else {
      setErrorMessage("Weak password");
    }
  };
  return (
    <div className="mb-3">
      <label htmlFor="passwordInput" className="form-label">
        Password
      </label>
      <input
        type={showPassword ? "text" : "password"}
        className="form-control"
        id="passwordInput"
        onChange={(e) => {
          validate(e.target.value);
          setPassword(e.target.value);
        }}
      />
      {errorMessage === "" ? null : (
        <div
          id="passwordHelpBlock"
          className={errorMessage === "" ? "form-text" : "text-warning"}
        >
          {errorMessage}
        </div>
      )}
      {confirmPassword && (
        <PasswordConfirmation
          passwordInput={password}
          showPassword={showPassword}
        />
      )}
      <div className="mb-3 form-check">
        <input
          type="checkbox"
          className="form-check-input"
          id="exampleCheck1"
          onClick={() => {
            setShowPassword(!showPassword);
          }}
        />
        <label className="form-check-label" htmlFor="exampleCheck1">
          Show password
        </label>
      </div>
    </div>
  );
};

export default PasswordInput;
