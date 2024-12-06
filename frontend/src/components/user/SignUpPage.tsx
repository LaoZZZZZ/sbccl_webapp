import React, { useContext, useState } from "react";
import PasswordInput from "../common/PasswordInput.tsx";
import EmailInput from "../common/EmailInput.tsx";
import TextInput from "../common/TextInput.tsx";
import validator from "validator";

import axios from "axios";
import { UserContext } from "../app/App.tsx";
import Alert from "../common/Alert.tsx";

interface Props {
  onBackToLogin: () => void;
}

const SignUpStatus = {
  SUCCESS: 0,
  FAILED: 1,
};

const sendSignUpRequest = async (user_info, callback) => {
  try {
    await axios.post(
      process.env.REACT_APP_BE_URL_PREFIX + "/rest_api/members/",
      user_info,
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    const confirm_msg =
      "Well done! You successfully created an account! An verification email has been sent to registered email";
    callback({
      status: SignUpStatus.SUCCESS,
      msg: confirm_msg,
      data: user_info,
    });
    return true;
  } catch (error) {
    callback({
      status: SignUpStatus.FAILED,
      msg: JSON.stringify(error.response.data.detail),
    });
    return false;
  }
};

const SignUpPage = ({ onBackToLogin }: Props) => {
  const [emailAddress, setEmailAddress] = useState("");
  const [password, setPassword] = useState("");
  const [lastName, setLastName] = useState("");
  const [firstName, setFirstName] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("000");
  const [memberType, setMemberType] = useState("");

  const [signUpStatus, setSignupStatus] = useState({});
  const [, dispatch] = useContext(UserContext);

  const onSignUp = () => {
    if (emailAddress === "") {
      setSignupStatus({
        status: SignUpStatus.FAILED,
        msg: "Please provide a valid email address!",
      });
      return;
    }
    if (password === "") {
      setSignupStatus({
        status: SignUpStatus.FAILED,
        msg: "Please enter a valid password!",
      });
      return;
    }
    if (firstName === "" || lastName === "") {
      setSignupStatus({
        status: SignUpStatus.FAILED,
        msg: "Please provide valid name!",
      });
      return;
    }
    if (phoneNumber === "") {
      setSignupStatus({
        status: SignUpStatus.FAILED,
        msg: "Please provide valid phone number!",
      });
      return;
    }
    const user_info = {
      username: emailAddress,
      email: emailAddress,
      password: password,
      last_name: lastName,
      first_name: firstName,
      member_type: memberType,
    };
    // The phone number is provided and validated.
    if (phoneNumber !== "") {
      user_info["phone_number"] = phoneNumber;
    }
    return sendSignUpRequest(user_info, setSignupStatus);
  };

  return (
    <div className="col w-50 mx-auto align-middle">
      <form className="form-label form-control">
        <EmailInput parentCallback={setEmailAddress} />
        <PasswordInput confirmPassword={true} retrievePassword={setPassword} />
        <TextInput
          labelText="First name"
          inputType={"text"}
          requiredInput={true}
          retrieveInput={setFirstName}
          validationFunc={(value) => {
            return validator.isAlpha(value);
          }}
        />
        <TextInput
          labelText="Last name"
          inputType={"text"}
          requiredInput={true}
          retrieveInput={setLastName}
          validationFunc={(value) => {
            return validator.isAlpha(value);
          }}
        />
        <div className="form-group pb-2">
          <label>
            <strong>*Account type</strong>
          </label>
          <select
            className="form-control"
            id="accountSelect"
            onChange={(e) => {
              setMemberType(e.target.value);
            }}
          >
            <option>Not Selected</option>
            <option>Parent</option>
            <option disabled>Teacher</option>
            <option disabled>Volunteer</option>
          </select>
        </div>
        <TextInput
          labelText="Phone number"
          inputType={"tel"}
          requiredInput={true}
          retrieveInput={setPhoneNumber}
          validationFunc={(phone_number) => {
            return validator.isMobilePhone(phone_number);
          }}
        />
        <div className="btn-group">
          <input
            className="btn btn-primary active mr-2"
            type="button"
            value="Sign up"
            onClick={() => {
              onSignUp();
            }}
          />
          <input
            className="btn btn-secondary ml-2"
            type="button"
            value="Back to login"
            onClick={() => {
              onBackToLogin();
            }}
          />
        </div>
      </form>
      {signUpStatus["status"] === SignUpStatus.FAILED && (
        <div>
          <Alert
            success={false}
            message={signUpStatus["msg"]}
            parentCallback={() => {
              setSignupStatus({});
            }}
          />
        </div>
      )}
      {signUpStatus["status"] === SignUpStatus.SUCCESS && (
        <div>
          <Alert
            success={true}
            message={signUpStatus["msg"]}
            parentCallback={() => {
              onBackToLogin();
            }}
          />
        </div>
      )}
    </div>
  );
};

export default SignUpPage;
