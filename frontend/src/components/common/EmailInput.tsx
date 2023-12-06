import React, { useState } from "react";
import validator from "validator";

interface Props {
  parentCallback: (boolean) => void;
}

const EmailInput = ({ parentCallback }: Props) => {
  let defaultMessage = "We'll never share your email with anyone else.";
  const [emailMessage, setEmailMessage] = useState(defaultMessage);
  return (
    <div>
      <label htmlFor="exampleInputEmail1" className="form-label">
        Email address
      </label>
      <input
        type="email"
        className="form-control"
        id="exampleInputEmail1"
        aria-describedby="emailHelp"
        required
        onChange={(e) => {
          let valid =
            e.target.value !== "" && validator.isEmail(e.target.value);
          if (!valid) {
            setEmailMessage("Invalid email format!");
          } else {
            setEmailMessage(defaultMessage);
          }
          parentCallback(valid);
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
    </div>
  );
};

export default EmailInput;
