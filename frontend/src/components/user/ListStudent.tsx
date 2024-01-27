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
    { column_name: "Last Name", key: "last_name" },
    { column_name: "First Name", key: "first_name" },
    { column_name: "Gender", key: "gender" },
    { column_name: "Date Of Birth", key: "date_of_birth" },
  ];

  return (
    <>
      <table className="table table-bordered table-hover">
        <thead>
          <tr>
            {table_columns_names.map((key_value) => {
              return <th scope="col">{key_value.column_name}</th>;
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
            <Student student={student_info} columns={table_columns_names} />
          ))}
        </tbody>
      </table>
    </>
  );
};

export default ListStudent;
