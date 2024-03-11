import axios from "axios";

const fetchRegistrations = async (user_info, callback) => {
  const response = await axios.get(
<<<<<<< HEAD
<<<<<<< HEAD
    process.env.REACT_APP_BE_URL_PREFIX +
=======
    "http://" +
      process.env.REACT_APP_BE_URL_PREFIX +
>>>>>>> a0582317 (Parameterize backend hostname.)
=======
    process.env.REACT_APP_BE_URL_PREFIX +
>>>>>>> 4e711736 (use https in remote deployment.)
      "/rest_api/members/list-registrations",
    {
      headers: {
        "Content-Type": "application/json",
      },
      auth: {
        username: user_info.auth.username,
        password: user_info.auth.password,
      },
    }
  );

  if (response.status === 200) {
    const registrations = response.data.registrations.map((json) => {
      return JSON.parse(json);
    });
    callback({
      fetched: true,
      value: registrations,
    });
    return;
  }

  callback({ fetched: true, value: [] });
};

export default fetchRegistrations;
