import React, { ReactNode } from "react";

interface Props {
  message: ReactNode;
  parentCallback: () => void;
}

export const Alert = ({ message, parentCallback }: Props) => {
  return (
    <div className="alert alert-danger alert-dismissible" role="alert">
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
