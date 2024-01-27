import React, { useEffect, useState } from "react";
import Student from "./Student.tsx";
import axios from "axios";

interface Props {
  userInfo: React.ReactNode;
}

interface StudentState {
  fetched: boolean;
  value: [];
}

const fetchStudents = async (user_info, callback) => {
  const response = await axios.get(
    "http://localhost:8000/rest_api/members/fetch-students",
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

  if (response.status == 200) {
    callback({
      fetched: true,
      value: response.data.students.map((json) => {
        return JSON.parse(json);
      }),
    });
  } else {
    callback({ fetched: false, value: [] });
  }
};

const ListStudent = ({ userInfo }: Props) => {
  const [studentsState, setStudentsState] = useState<StudentState>({
    fetched: false,
    value: [],
  });
  useEffect(() => {
    if (!studentsState.fetched) {
      fetchStudents(userInfo, setStudentsState);
    }
  }, [studentsState]);
  const table_columns_names = [
    "Last Name",
    "First Name",
    "Gender",
    "Date Of Birth",
  ];

  const keys = ["last_name", "first_name", "gender", "date_of_birth"];

  return (
    <>
      <table className="table table-bordered table-hover">
        <thead>
          <tr>
            {table_columns_names.map((colmunName) => {
              return <th scope="col">{colmunName}</th>;
            })}
            <th>
              <button type="button" className="btn btn-primary">
                Add Student
              </button>
            </th>
          </tr>
        </thead>
        <tbody>
          {studentsState.value.map((student_info) => (
            <Student student={student_info} columns={keys} />
          ))}
        </tbody>
      </table>
    </>
  );
};

export default ListStudent;
