import React, { useEffect, useState } from "react";
import axios from "axios";
import ListStudents from "./ListStudents.tsx";
import AddStudents from "./AddStudentsPage.tsx";

interface Props {
  userInfo: React.ReactNode;
}

interface StudentState {
  fetched: boolean;
  value: [];
  addStudent: boolean;
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
    const students = response.data.students.map((json) => {
      return JSON.parse(json);
    });

    callback({
      fetched: true,
      value: students,
    });
  } else {
    callback({ fetched: false, value: [] });
  }
};

const StudentsPage = ({ userInfo }: Props) => {
  const [studentsState, setStudentsState] = useState<StudentState>({
    fetched: false,
    value: [],
    addStudent: false,
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

  return (
    <>
      {studentsState.value.length > 0 && (
        <ListStudents students={studentsState.value} />
      )}
      {/* Add a divider to the remaining part of page */}
      <hr className="hr pt-2" />
      {!studentsState.addStudent && (
        <button
          type="button"
          className="btn btn-primary"
          onClick={() => {
            setStudentsState({
              ...studentsState,
              addStudent: true,
            });
          }}
        >
          Add Student
        </button>
      )}
      {studentsState.addStudent && (
        <AddStudents
          userAuth={userInfo.auth}
          updateStudentList={() => {
            setStudentsState({
              fetched: false,
              value: [],
              addStudent: false,
            });
          }}
        />
      )}
    </>
  );
};

export default StudentsPage;
