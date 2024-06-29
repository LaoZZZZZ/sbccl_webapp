import axios from "axios";

export interface UserDetails {
  last_name: string;
  first_name: string;
  user_name: string;
  email: string;
}

const fetchAccountDetails = async (auth, callback) => {
  await axios
    .get(
      process.env.REACT_APP_BE_URL_PREFIX + "/rest_api/members/account-details",
      {
        headers: {
          "Content-Type": "application/json",
        },
        auth: {
          username: auth.username,
          password: auth.password,
        },
      }
    )
    .then(function (response) {
      callback({
        fetched: true,
        value: response.data.account_details,
      });
      return;
    })
    .catch(function (error) {
      callback({ fetched: true, value: {} });
    });
};

export default fetchAccountDetails;
