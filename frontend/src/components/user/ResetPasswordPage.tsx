import React, { useContext, useState } from "react";
import EmailInput from "../common/EmailInput.tsx";
import axios from "axios";
import { UserContext } from "../app/App.tsx";
import Alert from "../common/Alert.tsx";

interface Props {
  onBackToLogin: () => void;
}

const Status = {
  SUCCESS: 0,
  FAILED: 1,
};
const ResetPasswordPage = ({ onBackToLogin }: Props) => {
  const [emailAddress, setEmailAddress] = useState("");
  const [, dispatch] = useContext(UserContext);
  const [resetStatus, setResetStatus] = useState({});

  return (
    <>
      <form className="row g-3">
        <EmailInput parentCallback={setEmailAddress} />
        <div className="col-auto">
          <button
            type="submit"
            className="btn btn-primary"
            onClick={async () => {
              if (emailAddress === "") {
                setResetStatus({
                  status: Status.FAILED,
                  msg: "No email is provided",
                });
                return;
              }
              const url =
                "http://localhost:8000/rest_api/members/" +
                emailAddress +
                "/create-password-reset-code/";
              console.log("url: " + url);
              await axios
                .put(url)
                .then(function (response) {
                  // reset password is
                  if (response.status == 201) {
                    console.log();
                    setResetStatus({
                      status: Status.SUCCESS,
                      msg: "A password reset link has been sent to your registred email.",
                    });
                  }
                })
                .catch(function (error) {
                  console.log("error: " + error.response.data);
                  setResetStatus({
                    status: Status.FAILED,
                    msg: JSON.stringify(error.response.data),
                  });
                });
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
      {resetStatus["status"] === Status.FAILED && (
        <Alert
          success={false}
          message={resetStatus["msg"]}
          parentCallback={() => {
            setResetStatus({});
          }}
        />
      )}
      {resetStatus["status"] === Status.SUCCESS && (
        <Alert
          success={true}
          message={resetStatus["msg"]}
          parentCallback={() => {
            // dispatch({ type: "login" });
          }}
        />
      )}
    </>
  );
};

export default ResetPasswordPage;
