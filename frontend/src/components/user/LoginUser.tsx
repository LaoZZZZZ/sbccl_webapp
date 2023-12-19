import { useContext, useEffect } from "react";
import PropTypes from "prop-types";
import { UserContext } from "../app/App";
import axios from "axios";

export const LoginUser = ({ username, password }) => {
  const [, dispatch] = useContext(UserContext);

  useEffect(() => {
    const login = async () => {
      const response = await axios.put(
        "http://localhost:8000/rest_api/members/login/",
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
