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

export interface CourseList {
  fetched: boolean;
  courses: ClassInformation[];
}
// Find course in courses that is suffix of the course name shown on the screen.
// @courseName: It's the name shown on the screen, and might be different from the actual name
export const findSelectedCourse = (courses, courseName) => {
  const selected_course = courses.filter((course) =>
    courseName.endsWith(course.name)
  );
  if (selected_course.length === 1) {
    return selected_course[0];
  }
  return null;
};

export const extractCourseTime = (course: ClassInformation) => {
  // A random date to form a valid Date instance.
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

export const fetchCourses = async (
  auth: Auth,
  school_start,
  school_end,
  callback
) => {
  var url = "/rest_api/members/list-courses/";
  if (school_start > 0 && school_end > 0) {
    url = url + `?school_start=${school_start}&school_end=${school_end}`;
  }

  const response = await axios.get(process.env.REACT_APP_BE_URL_PREFIX + url, {
    headers: {
      "Content-Type": "application/json",
    },
    auth: {
      username: auth.username,
      password: auth.password,
    },
  });

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
