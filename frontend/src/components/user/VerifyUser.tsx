import React, { useState } from "react";
import { redirect, redirectDocument, useParams } from "react-router-dom";
import EmailInput from "../common/EmailInput.tsx";
import axios from "axios";
import Alert from "../common/Alert.tsx";

const VerificatiionStatus = {
  SUCCESS: 0,
  FAILED: 1,
};

// Send verify-user request to backend to verify the user.
//
const sendUserVerificationRequest = async (user_info, callback) => {
  try {
    const response = await axios.put(
      "http://localhost:8000/rest_api/members/verify-user/",
      null,
      {
        headers: {
          "Content-Type": "application/json",
        },
        params: user_info,
      }
    );
    const confirm_msg =
      "Well done! Your account has been successfully verified and ready for use!";
    callback({
      status: VerificatiionStatus.SUCCESS,
      msg: confirm_msg,
    });
    return true;
  } catch (e) {
    callback({
      status: VerificatiionStatus.FAILED,
      msg: JSON.stringify(e.response.data),
    });
    return false;
  }
};

const VerifyUser = () => {
  let { verification_code } = useParams();
  const [emailAddress, setEmailAddress] = useState("");
  const [verificationStatus, setVerificationStatus] = useState({});

  const onVerify = () => {
    if (emailAddress === "") {
      setVerificationStatus({
        status: VerificatiionStatus.FAILED,
        msg: "Please provide a valid email address!",
      });
      return;
    }
    const user_info = {
      email: emailAddress,
      verification_code: verification_code,
    };
    return sendUserVerificationRequest(user_info, setVerificationStatus);
  };

  return (
    <>
      <div className="container">
        <form className="w-50 form-control">
          <div className="form-group mb-2">
            <EmailInput parentCallback={setEmailAddress} />
            <input
              className="btn btn-primary active"
              type="button"
              value="Verify"
              onClick={() => {
                onVerify();
              }}
            />
          </div>
        </form>
        {verificationStatus["status"] === VerificatiionStatus.FAILED && (
          <Alert
            success={false}
            message={verificationStatus["msg"]}
            parentCallback={() => {
              setVerificationStatus({});
            }}
          />
        )}
        {verificationStatus["status"] === VerificatiionStatus.SUCCESS && (
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

export default VerifyUser;