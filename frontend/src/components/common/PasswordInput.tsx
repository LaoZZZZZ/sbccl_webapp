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
        required
        onChange={(e) => {
          matchPassword(passwordInput, e.target.value);
        }}
      />
      {errorMessage === "" ? null : (
        <div
          id="passwordHelpBlock"
          className={errorMessage === "" ? "form-text" : "text-danger"}
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
  retrievePassword: (string) => void;
}

const PasswordInput = ({ confirmPassword, retrievePassword }: Props) => {
  const defaultText =
    "Must be at least 8 characters long, contain lower, upper case letters and digits";
  const [errorMessage, setErrorMessage] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [password, setPassword] = useState("");

  const validate = (password) => {
    if (
      validator.isStrongPassword(password, {
        minLength: 8,
        minNumbers: 1,
        minLowercase: 1,
        minUppercase: 1,
        minSymbols: 0,
      })
    ) {
      setErrorMessage("");
      return true;
    } else {
      setErrorMessage("Invalid password");
      return false;
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
          if (validate(e.target.value)) {
            setPassword(e.target.value);
            retrievePassword(e.target.value);
          }
        }}
        required
      />
      <div
        id="passwordHelpBlock"
        className={errorMessage === "" ? "form-text" : "text-danger"}
      >
        {errorMessage === "" ? defaultText : errorMessage}
      </div>

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
          required
          onChange={(event) => {
            setShowPassword(event.target.checked);
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
