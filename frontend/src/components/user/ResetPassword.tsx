import React, { useState } from "react";
import EmailInput from "../common/EmailInput.tsx";

interface Props {
  onReset: (boolean) => void;
  onBackToLogin: () => void;
}

const ResetPassword = ({ onReset, onBackToLogin }: Props) => {
  const [isEmailValid, setIsEmailValid] = useState(false);
  return (
    <>
      <form className="row g-3">
        <EmailInput parentCallback={setIsEmailValid} />
        <div className="col-auto">
          <button
            type="submit"
            className="btn btn-primary"
            onClick={() => {
              if (isEmailValid) {
                onReset(true);
              }
            }}
          >
            Reset
          </button>
          <input
            className="btn btn-secondary"
            type="button"
            value="Back to login"
            onClick={() => {
              onBackToLogin();
            }}
          />
        </div>
      </form>
    </>
  );
};

export default ResetPassword;
