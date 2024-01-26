import React, { useState } from "react";
import { redirect, redirectDocument, useParams } from "react-router-dom";
import EmailInput from "../common/EmailInput.tsx";
import axios from "axios";
import Alert from "../common/Alert.tsx";
import PasswordInput from "../common/PasswordInput.tsx";

const PasswordResetStatus = {
  SUCCESS: 0,
  FAILED: 1,
};

// Send reset-password-by-code/?reset_code={code}&emai={email}&password={password} to
// backend.
const sendPasswordResetRequest = async (user_info, callback) => {
  try {
    const response = await axios.put(
      "http://localhost:8000/rest_api/members/reset-password-by-code/",
      null,
      {
        headers: {
          "Content-Type": "application/json",
        },
        params: user_info,
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

  const onVerify = () => {
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
                onVerify();
              }}
            />
          </div>
        </form>
        {verificationStatus["status"] === PasswordResetStatus.FAILED && (
          <Alert
            success={false}
            message={verificationStatus["msg"]}
            parentCallback={() => {
              setVerificationStatus({});
            }}
          />
        )}
        {verificationStatus["status"] === PasswordResetStatus.SUCCESS && (
          <Alert
            success={true}
            message={verificationStatus["msg"]}
            parentCallback={() => {
              console.log("Redirect to login");
              return redirect("/login");
            }}
          />
        )}
      </div>
    </>
  );
};

export default ResetPasswordByCode;
