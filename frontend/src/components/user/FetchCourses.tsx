import axios from "axios";

const fetchCourses = async (user_info, callback) => {
  const response = await axios.get(
    process.env.REACT_APP_BE_URL_PREFIX + "/rest_api/members/list-courses",
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
