import axios from "axios";
import { Auth } from "./UserInfo";

const signTerms = async (auth: Auth, callback) => {
  const response = await axios.put(
    process.env.REACT_APP_BE_URL_PREFIX + "/rest_api/members/sign-terms",
    {
      headers: {
        "Content-Type": "application/json",
      },
      auth: {
        username: auth.username,
        password: auth.password,
      },
    }
  );

  if (response.status === 202) {
    return true;
  }

  return false;
};

export default signTerms;
