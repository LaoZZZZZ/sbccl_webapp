import axios from "axios";

const fetchStudents = async (user_info, callback) => {
  const response = await axios.get(
    "http://" +
      process.env.REACT_APP_BE_URL_PREFIX +
      "/rest_api/members/fetch-students",
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
    const students = response.data.students.map((json) => {
      return JSON.parse(json);
    });

    callback({
      fetched: true,
      value: students,
    });
    return;
  }
  callback({ fetched: true, value: [] });
};

export default fetchStudents;
