import axios from "axios";
import React from "react";
import Student from "./Student.tsx";

interface Props {
  userInfo: React.ReactNode;
}

const fetchStudents = async (user_info) => {
  try {
    const response = await axios.get(
      "http://localhost:8000/rest_api/members/get-students",
      {
        headers: {
          "Content-Type": "application/json",
        },
        auth: {
          username: user_info.user.username,
          password: user_info.password,
        },
      }
    );
    return response.data;
  } catch (error) {
    return ["abc", "edf"];
    return error.response.data;
  }
};

const ListStudent = ({ userInfo }: Props) => {
  console.log(userInfo);
  let students = fetchStudents(userInfo);

  let studentElements = students.map(function (student_info) {
    return <div>{<Student student={student_info} />}</div>;
  });
  return <div>{studentElements}</div>;
};

export default ListStudent;
