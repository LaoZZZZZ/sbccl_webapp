import React, { useContext, useState } from "react";
import PasswordInput from "../common/PasswordInput.tsx";
import EmailInput from "../common/EmailInput.tsx";
import TextInput from "../common/TextInput.tsx";

import axios from "axios";
import { UserContext } from "../app/App.tsx";
import Alert from "../common/Alert.tsx";

const userSignUp = async (user_profile) => {
  const userLoginResponse = await axios
    .put("http://localhost:8000/rest_api/members/sign-up", {
      user_profile,
    })
    .then(function (response) {
      console.log(response);
      if (response.status == 200) {
        return {
          page: Page.StartLogin,
          // Add students here.
        };
      } else {
        return {
          page: Page.StartSignUp,
          // Add students here.
        };
      }
    });
};

interface Props {
  // login
  onBackToLogin: () => void;
}

const SignUpStatus = {
  SUCCESS: 0,
  FAILED: 1,
};

const SignUpPage = ({ onBackToLogin }: Props) => {
  const [emailAddress, setEmailAddress] = useState("");
  const [password, setPassword] = useState("");
  const [lastName, setLastName] = useState("");
  const [firstName, setFirstName] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");

  const [signUpStatus, setSignupStatus] = useState({});
  const [, dispatch] = useContext(UserContext);

  return (
    <div>
      <form className="needs-validation">
        <EmailInput parentCallback={setEmailAddress} />
        <PasswordInput confirmPassword={true} retrievePassword={setPassword} />
        <TextInput
          labelText="First name"
          inputType={"text"}
          requiredInput={true}
          retrieveInput={setFirstName}
        />
        <TextInput
          labelText="Last name"
          inputType={"text"}
          requiredInput={true}
          retrieveInput={setLastName}
        />
        <TextInput
          labelText="Cell phone"
          inputType={"tel"}
          requiredInput={false}
          retrieveInput={setPhoneNumber}
        />
        <input
          className="btn btn-primary active"
          type="button"
          value="Sign up"
          onClick={async () => {
            if (emailAddress === "" || password === "") {
              setSignupStatus({
                status: SignUpStatus.FAILED,
                msg: "Invalid information is provided!",
              });
              return;
            }
            console.log("email: " + emailAddress + " password: " + password);
            const user_info = {
              username: emailAddress,
              email: emailAddress,
              password: password,
              last_name: lastName,
              first_name: firstName,
              phone_number: phoneNumber,
            };
            await axios
              .post("http://localhost:8000/rest_api/members/", user_info, {
                headers: {
                  "Content-Type": "application/json",
                },
              })
              .then(function (response) {
                console.log(response);
                if (response.status == 201) {
                  setSignupStatus({
                    status: SignUpStatus.SUCCESS,
                    msg: "Well done! You successfully created an account!",
                    data: user_info,
                  });
                }
              })
              .catch(function (error) {
                console.log(error);
                setSignupStatus({
                  status: SignUpStatus.FAILED,
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
            onBackToLogin();
          }}
        />
      </form>
      {signUpStatus["status"] === SignUpStatus.FAILED && (
        <Alert
          success={false}
          message={signUpStatus["msg"]}
          parentCallback={() => {
            setSignupStatus({});
          }}
        />
      )}
      {signUpStatus["status"] === SignUpStatus.SUCCESS && (
        <Alert
          success={true}
          message={signUpStatus["msg"]}
          parentCallback={() => {
            dispatch({ type: "login", user_info: signUpStatus["data"] });
          }}
        />
      )}
    </div>
  );
};

export default SignUpPage;
