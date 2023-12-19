import React from "react";

interface Props {
  onSubmit: () => void;
  onSignUp: () => void;
  onResetPassword: () => void;
}

const UserButtons = ({ onSubmit, onSignUp, onResetPassword }: Props) => {
  return (
    <div className="btn-group">
      <input
        className="btn btn-primary active"
        type="button"
        value="Login"
        onClick={() => {
          onSubmit();
        }}
      />
      <input
        className="btn btn-primary"
        type="button"
        value="Sign Up"
        onClick={() => {
          onSignUp();
        }}
      />
      <input
        className="btn btn-secondary"
        type="button"
        value="Reset Password"
        onClick={() => {
          onResetPassword();
        }}
      />
    </div>
  );
};

export default UserButtons;
