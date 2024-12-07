import React, { useState } from "react";
import validator from "validator";

interface Props {
  parentCallback: (string) => void;
}

const EmailInput = ({ parentCallback }: Props) => {
  let defaultMessage = "We'll never share your email with anyone else.";
  const [emailMessage, setEmailMessage] = useState(defaultMessage);
  return (
    <>
      <label htmlFor="exampleInputEmail1" className="form-label">
        <strong>*Email address</strong>
      </label>
      <input
        type="email"
        className="form-control"
        id="exampleInputEmail1"
        aria-describedby="emailHelp"
        autoComplete="username"
        required
        onChange={(e) => {
          let valid =
            e.target.value !== "" && validator.isEmail(e.target.value);
          if (!valid) {
            setEmailMessage("Invalid email format!");
            parentCallback("");
          } else {
            setEmailMessage(defaultMessage);
            parentCallback(e.target.value);
          }
        }}
      />
      <div
        id="emailHelp"
        className={
          emailMessage === defaultMessage ? "form-text" : "text-warning"
        }
      >
        {emailMessage}
      </div>
    </>
  );
};

export default EmailInput;
