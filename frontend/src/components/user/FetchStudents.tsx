import axios from "axios";

const fetchStudents = async (user_info, callback) => {
  const response = await axios.get(
<<<<<<< HEAD
<<<<<<< HEAD
    process.env.REACT_APP_BE_URL_PREFIX + "/rest_api/members/fetch-students",
=======
    "http://" +
      process.env.REACT_APP_BE_URL_PREFIX +
      "/rest_api/members/fetch-students",
>>>>>>> a0582317 (Parameterize backend hostname.)
=======
    process.env.REACT_APP_BE_URL_PREFIX + "/rest_api/members/fetch-students",
>>>>>>> 4e711736 (use https in remote deployment.)
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
