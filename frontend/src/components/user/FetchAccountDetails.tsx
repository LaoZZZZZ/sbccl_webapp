import axios from "axios";

const fetchAccountDetails = async (user_info, callback) => {
  await axios
    .get(
      process.env.REACT_APP_BE_URL_PREFIX + "/rest_api/members/account-details",
      {
        headers: {
          "Content-Type": "application/json",
        },
        auth: {
          username: user_info.auth.username,
          password: user_info.auth.password,
        },
      }
    )
    .then(function (response) {
      callback({
        fetched: true,
        value: JSON.parse(response.data.account_details),
      });
    })
    .catch(function (error) {
      console.log(error);
      callback({ fetched: true, value: {} });
    });
};

export default fetchAccountDetails;
