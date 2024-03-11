import React, { useContext, useState } from "react";
import EmailInput from "../common/EmailInput.tsx";
import axios from "axios";
import { UserContext } from "../app/App.tsx";
import Alert from "../common/Alert.tsx";

interface Props {
  onBackToLogin: () => void;
}

const Status = {
  UNSPECIFIED: 0,
  SUCCESS: 1,
  FAILED: 2,
};

const ResetPasswordPage = ({ onBackToLogin }: Props) => {
  const [emailAddress, setEmailAddress] = useState("");
  const [, dispatch] = useContext(UserContext);
  const [resetStatus, setResetStatus] = useState({
    status: Status.UNSPECIFIED,
    msg: "",
  });

  return (
    <div>
      <form className="w-50 form-control">
        <EmailInput parentCallback={setEmailAddress} />
        <input
          className="btn btn-primary active"
          type="button"
          value="Reset"
          onClick={async () => {
            if (emailAddress === "") {
              setResetStatus({
                status: Status.FAILED,
                msg: "No valid email is provided",
              });
              return;
            }
            const url =
<<<<<<< HEAD
=======
              "http://" +
>>>>>>> a0582317 (Parameterize backend hostname.)
              process.env.REACT_APP_BE_URL_PREFIX +
              "/rest_api/members/create-password-reset-code/?email=" +
              emailAddress;
            await axios
              .put(url, {}, {})
              .then(function (response) {
                // reset code is created successfully.
                if (response.status == 201) {
                  setResetStatus({
                    status: Status.SUCCESS,
                    msg: "A password reset link has been sent to your registred email.",
                  });
                }
              })
              .catch(function (error) {
                console.log(error.response.data);
                setResetStatus({
                  status: Status.FAILED,
                  msg: JSON.stringify(error.response.data),
                });
              });
          }}
        />
        <input
          className="btn btn-secondary"
          type="button"
          value="Back to login"
          onClick={() => {
            setResetStatus({
              status: Status.UNSPECIFIED,
              msg: "",
            });
            onBackToLogin();
          }}
        />
      </form>
      {resetStatus["status"] !== Status.UNSPECIFIED && (
        <Alert
          success={resetStatus["status"] === Status.SUCCESS}
          message={resetStatus["msg"]}
          parentCallback={() => {
            if (resetStatus["status"] == Status.SUCCESS) {
              onBackToLogin();
            } else {
              setResetStatus({
                status: Status.UNSPECIFIED,
                msg: "",
              });
            }
          }}
        />
      )}
    </div>
  );
};

export default ResetPasswordPage;
