import axios from "axios";
import { Auth } from "./UserInfo";

export interface ClassInformation {
  enrollment: number;
  size_limit: number;
  teacher: string;
  cost: number;
  course_type: string;
  classroom: string;
  course_start_time: string;
  course_end_time: string;
  book_cost: number;
  course_description: string;
  name: string;
  id: number;
}

export const extractCourseTime = (course: ClassInformation) => {
  var start = new Date("2024-10-01T" + course.course_start_time);
  var end = new Date("2024-10-01T" + course.course_end_time);
  return (
    start.toLocaleString("en-US", {
      hour: "numeric",
      hour12: true,
      minute: "numeric",
    }) +
    " - " +
    end.toLocaleString("en-US", {
      hour: "numeric",
      hour12: true,
      minute: "numeric",
    })
  );
};

export const getShownName = (course: ClassInformation) => {
  if (course.course_type === "E") {
    return "Enrichment - " + course.name;
  } else if (course.course_type === "L") {
    return "Language - " + course.name;
  } else {
    return course.name;
  }
};

const fetchCourses = async (auth: Auth, callback) => {
  const response = await axios.get(
    process.env.REACT_APP_BE_URL_PREFIX + "/rest_api/members/list-courses",
    {
      headers: {
        "Content-Type": "application/json",
      },
      auth: {
        username: auth.username,
        password: auth.password,
      },
    }
  );

  if (response.status === 200) {
    const courses = response.data.courses.map(JSON.parse);
    courses.sort((a, b) => {
      if (a.course_type < b.course_type) {
        return -1;
      } else if (a.course_type > b.course_type) {
        return 1;
      }
      if (a.name < b.name) {
        return -1;
      }
      return 1;
    });
    callback({
      fetched: true,
      courses: courses,
    });
    return;
  }

  callback({ fetched: true, value: [] });
};

export default fetchCourses;
