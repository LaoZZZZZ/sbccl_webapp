import axios from "axios";
import { Auth } from "./UserInfo";

// Used for parent account
export interface Student {
  first_name: string;
  last_name: string;
  middle_name: string;
  gender: string;
  date_of_birth: Date;
  joined_date: Date;
  chinese_name: string;
}

// Used for teacher and board member account
export interface Contact {
  parent: string; // Name of parent
  email: string;
  phone: string;
}

export interface RosterStudent {
  first_name: string;
  last_name: string;
  middle_name: string;
  gender: string;
  joined_date: Date;
  chinese_name: string;
  age: number;
  contact: Contact;
  on_waiting_list: boolean;
}

export const fetchStudents = async (user_info, callback) => {
  const response = await axios.get(
    process.env.REACT_APP_BE_URL_PREFIX + "/rest_api/members/fetch-students",
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

export const FetchCourseRoster = async (
  auth: Auth,
  course_id: Number,
  callback
) => {
  const response = await axios.get(
    process.env.REACT_APP_BE_URL_PREFIX +
      "/rest_api/members/" +
      course_id.toString() +
      "/list-students-per-class",
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
    const roster = response.data.students.map((stu) => {
      const student: RosterStudent = JSON.parse(stu);
      student.contact = JSON.parse(student.contact);
      return student;
    });
    callback({
      fetched: true,
      students: roster,
    });
    return;
  }
  callback({ fetched: true, students: [] });
};
