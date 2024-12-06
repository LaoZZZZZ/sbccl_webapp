import { useEffect } from "react";
import PropTypes from "prop-types";
import axios from "axios";

export const LoginUser = ({ username, password }) => {
  useEffect(() => {
    const login = async () => {
      const response = await axios.put(
        process.env.REACT_APP_BE_URL_PREFIX + "/rest_api/members/login/",
        {},
        {
          auth: {
            username: username,
            password: password,
          },
        }
      );

      if (response.status == 202) {
        const user_info = response.data;
        dispatch({ type: 0, user_info });
      } else {
        const user_info = null;
        dispatch({ type: 0, user_info });
      }
    };
    login();
  }, [username, password, dispatch]);
  return null;
};

LoginUser.propTypes = {
  username: PropTypes.string,
  password: PropTypes.string,
  // Will be set if session token is enabled.
  // auth_token: PropTypes.string
};
