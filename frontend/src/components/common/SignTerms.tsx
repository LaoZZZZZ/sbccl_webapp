import axios from "axios";
import { Auth } from "../user/UserInfo";

const signTerms = async (userAuth: Auth, successCallback, failureCallback) => {
  await axios
    .put(
      process.env.REACT_APP_BE_URL_PREFIX + "/rest_api/members/sign-terms/",
      {},
      {
        auth: userAuth,
      }
    )
    .then((response) => {
      successCallback();
      return true;
    })
    .catch((error) => {
      failureCallback();
      return false;
    });
};

export default signTerms;
