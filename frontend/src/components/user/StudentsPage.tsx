import React, { useEffect, useState } from "react";
import ListStudents from "./ListStudents.tsx";
import AddStudents from "./AddStudentsPage.tsx";
import fetchStudents from "./FetchStudents.tsx";
import UserInfo from "./UserInfo.tsx";

interface Props {
  userInfo: UserInfo;
}

interface StudentState {
  fetched: boolean;
  value: [];
  addStudent: boolean;
}

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

  // The students list has changed. Trigger refetching from the backend.
  const fetchStudentLists = () => {
    setStudentsState({
      fetched: false,
      value: [],
      addStudent: false,
    });
  };

  return (
    <>
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
      <hr className="hr pt-2" />
      {studentsState.addStudent && (
        <AddStudents
          userAuth={userInfo.auth}
          updateStudentList={fetchStudentLists}
        />
      )}
      {/* Add a divider to the remaining part of page */}

      {!studentsState.addStudent && studentsState.value.length > 0 && (
        <ListStudents
          students={studentsState.value}
          userAuth={userInfo.auth}
          updateStudentList={fetchStudentLists}
        />
      )}
    </>
  );
};

export default StudentsPage;
