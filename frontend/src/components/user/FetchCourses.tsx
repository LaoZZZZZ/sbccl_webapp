import axios from "axios";

const fetchCourses = async (user_info, callback) => {
  const response = await axios.get(
<<<<<<< HEAD
<<<<<<< HEAD
    process.env.REACT_APP_BE_URL_PREFIX + "/rest_api/members/list-courses",
=======
    "http://" +
      process.env.REACT_APP_BE_URL_PREFIX +
      "/rest_api/members/list-courses",
>>>>>>> a0582317 (Parameterize backend hostname.)
=======
    process.env.REACT_APP_BE_URL_PREFIX + "/rest_api/members/list-courses",
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
    const courses = response.data.courses.map((json) => {
      return JSON.parse(json);
    });

    callback({
      fetched: true,
      value: courses,
    });
    return;
  }

  callback({ fetched: true, value: [] });
};

export default fetchCourses;
