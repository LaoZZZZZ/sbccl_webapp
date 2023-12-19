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
  onSubmit: (boolean) => void;
  onBackToLogin: () => void;
}

const SignUpPage = ({ onSubmit, onBackToLogin }: Props) => {
  const [emailAddress, setEmailAddress] = useState("");
  const [password, setPassword] = useState("");
  const [lastName, setLastName] = useState("");
  const [firstName, setFirstName] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");

  const [signupFailMsg, setSignupFailedMsg] = useState("");
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
              setSignupFailedMsg("Invalid information is provided!");
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
                if (response.status == 200) {
                  dispatch({ action: 0, user_info });
                }
              })
              .catch(function (error) {
                console.log(error);
                setSignupFailedMsg(error.message);
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
      {signupFailMsg !== "" && (
        <Alert
          message={signupFailMsg}
          parentCallback={() => {
            setSignupFailedMsg("");
          }}
        />
      )}
    </div>
  );
};

export default SignUpPage;
