import axios from "axios";

const fetchRegistrations = async (user_info, callback) => {
  const response = await axios.get(
    "http://localhost:8000/rest_api/members/list-registrations",
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
