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
    <div className="form-label">
      <label htmlFor="passwordConfirm" className="form-label">
        <strong>Confirm password</strong>
      </label>
      <input
        type={showPassword ? "text" : "password"}
        className="form-control"
        id="passwordConfirm"
        required
        autoComplete="new-password"
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
    </div>
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
      setErrorMessage(defaultText);
      return false;
    }
  };
  return (
    <>
      <div>
        <label htmlFor="passwordInput" className="form-label">
          <strong>*Password</strong>
        </label>
        <input
          type={showPassword ? "text" : "password"}
          className="form-control"
          id="passwordInput"
          autoComplete={confirmPassword ? "current-password" : "new-password"}
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
          className={errorMessage === "" ? "form-text" : "text-warning"}
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
            id="showpassword"
            onChange={(event) => {
              setShowPassword(event.target.checked);
            }}
          />
          <label className="form-check-label" htmlFor="exampleCheck1">
            Show password
          </label>
        </div>
      </div>
    </>
  );
};

export default PasswordInput;
