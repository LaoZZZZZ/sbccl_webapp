import React, { useState } from "react";

interface Props {
  userInfo: React.ReactNode;
}

interface PageState {
  fetched: boolean;
  value: [];
  addRegistration: boolean;
}

const Registration = ({ userInfo }: Props) => {
  const [pageState, setPageState] = useState<PageState>({
    fetched: false,
    value: [],
    addRegistration: false,
  });
  return (
    <>
      <p>Active Registrations!</p>
      <hr className="pb-2" />
      {!pageState.addRegistration && (
        <button
          type="button"
          className="btn btn-primary"
          onClick={() => {
            setPageState({
              ...pageState,
              addRegistration: true,
            });
          }}
        >
          Register Student
        </button>
      )}
      <hr className="pb-2" />
      <p>Past Registrations</p>
    </>
  );
};

export default Registration;
