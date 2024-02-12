import axios from "axios";

const Logout = async (userInfo, logOutCallback) => {
  await axios
    .put(
      "http://localhost:8000/rest_api/members/logout/",
      {},
      {
        auth: userInfo.auth,
      }
    )
    .then(function (response) {
      if (response.status == 202) {
        logOutCallback();
      }
    })
    .catch(function (error) {
      logOutCallback();
    });
};

export default Logout;
