import axios from "axios";

const Logout = async (userInfo, logOutCallback) => {
  await axios
    .put(
<<<<<<< HEAD
<<<<<<< HEAD
      process.env.REACT_APP_BE_URL_PREFIX + "/rest_api/members/logout/",
=======
      "http://" +
        process.env.REACT_APP_BE_URL_PREFIX +
        "/rest_api/members/logout/",
>>>>>>> a0582317 (Parameterize backend hostname.)
=======
      process.env.REACT_APP_BE_URL_PREFIX + "/rest_api/members/logout/",
>>>>>>> 4e711736 (use https in remote deployment.)
      {},
      {
        auth: userInfo.auth,
      }
    )
    .then(function (response) {
      if (response.status === 202) {
        logOutCallback();
      }
    })
    .catch(function (error) {
      logOutCallback();
    });
};

export default Logout;
