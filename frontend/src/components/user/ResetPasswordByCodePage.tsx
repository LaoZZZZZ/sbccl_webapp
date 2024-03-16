import React, { useState } from "react";
import { useParams } from "react-router-dom";
import EmailInput from "../common/EmailInput.tsx";
import axios from "axios";
import Alert from "../common/Alert.tsx";
import PasswordInput from "../common/PasswordInput.tsx";
import { useNavigate } from "react-router-dom";

const PasswordResetStatus = {
  SUCCESS: 0,
  FAILED: 1,
};

// Send reset-password-by-code/?reset_code={code}&emai={email}&password={password} to
// backend.
const sendPasswordResetRequest = async (user_info, callback) => {
  try {
    const response = await axios.put(
      process.env.REACT_APP_BE_URL_PREFIX +
        "/rest_api/members/reset-password-by-code/",
      null,
      {
        headers: {
          "Content-Type": "application/json",
        },
        params: user_info,
        // TODO: remove this for production deployment
        httpsAgent: new https.Agent({
          rejectUnauthorized: process.env.NODE_ENV === "prod",
        }),
      }
    );
    const confirm_msg =
      "Well done! Your account's password has been reset successfully!";
    callback({
      status: PasswordResetStatus.SUCCESS,
      msg: confirm_msg,
    });
    return true;
  } catch (e) {
    callback({
      status: PasswordResetStatus.FAILED,
      msg: JSON.stringify(e.response.data),
    });
    return false;
  }
};

const ResetPasswordByCode = () => {
  let { verification_code } = useParams();
  const [emailAddress, setEmailAddress] = useState("");
  const [password, setPassword] = useState("");
  const [verificationStatus, setVerificationStatus] = useState({});
  const navigate = useNavigate();

  const onReset = () => {
    if (emailAddress === "") {
      setVerificationStatus({
        status: PasswordResetStatus.FAILED,
        msg: "Please provide a valid email address!",
      });
      return;
    }
    const user_info = {
      email: emailAddress,
      password: password,
      verification_code: verification_code,
    };
    return sendPasswordResetRequest(user_info, setVerificationStatus);
  };

  return (
    <>
      <div className="container">
        <form className="w-50 form-control">
          <div className="form-group mb-2">
            <EmailInput parentCallback={setEmailAddress} />
            <PasswordInput
              confirmPassword={true}
              retrievePassword={setPassword}
            />
            <input
              className="btn btn-primary active"
              type="button"
              value="Reset"
              onClick={() => {
                onReset();
              }}
            />
          </div>
        </form>
        {verificationStatus["status"] === PasswordResetStatus.FAILED && (
          <Alert
            success={false}
            message={verificationStatus["msg"]}
            parentCallback={() => {
              navigate("/login");
            }}
          />
        )}
        {verificationStatus["status"] === PasswordResetStatus.SUCCESS && (
          <Alert
            success={true}
            message={verificationStatus["msg"]}
            parentCallback={() => {
              navigate("/login");
            }}
          />
        )}
      </div>
    </>
  );
};

export default ResetPasswordByCode;
