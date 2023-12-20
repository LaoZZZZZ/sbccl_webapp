import React, { ReactNode } from "react";

interface Props {
  success?: boolean;
  message: ReactNode;
  parentCallback: () => void;
}

export const Alert = ({ success, message, parentCallback }: Props) => {
  return (
    <div
      className={
        success
          ? "alert alert-success alert-dismissible"
          : "alert alert-danger alert-dismissible"
      }
      role="alert"
    >
      {message}
      <button
        type="button"
        className="btn-close"
        data-bs-dismiss="alert"
        aria-label="Close"
        onClick={parentCallback}
      ></button>
    </div>
  );
};

export default Alert;
