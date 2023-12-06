import React, { useState } from "react";
import EmailInput from "../common/EmailInput.tsx";

interface Props {
  onReset: (boolean) => void;
}

const ResetPassword = ({ onReset }: Props) => {
  const [isEmailValid, setIsEmailValid] = useState(false);
  return (
    <>
      <form className="row g-3">
        <EmailInput parentCallback={setIsEmailValid} />
        <div className="col-auto">
          <button
            type="submit"
            className="btn btn-primary mb-3"
            onClick={() => {
              console.log("email valided" + isEmailValid);
              if (isEmailValid) {
                onReset(true);
              }
            }}
          >
            Reset
          </button>
        </div>
      </form>
    </>
  );
};

export default ResetPassword;
