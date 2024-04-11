import React, { useEffect, useState } from "react";
import RemoveStudents from "./RemoveStudentsPage.tsx";
import AddStudents from "./AddStudentsPage.tsx";
import fetchStudents from "./FetchStudents.tsx";
import UserInfo from "./UserInfo.tsx";

interface Props {
  userInfo: UserInfo;
}

const Page = {
  ListStudent: 0, // User is on login page
  AddStudent: 1, // User is on reset password page
  RemoveStudent: 2, // user is on the sign up page
};

interface StudentState {
  fetched: boolean;
  value: [];
}

const StudentsPage = ({ userInfo }: Props) => {
  const [studentsState, setStudentsState] = useState<StudentState>({
    fetched: false,
    value: [],
  });

  const [pageState, setPageState] = useState(Page.ListStudent);

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
    });
    setPageState(Page.ListStudent);
  };

  const [removeStudent, setRemoveStudent] = useState({
    needRemoval: false,
    student: {},
  });

  const table_columns_names = [
    "Last Name",
    "First Name",
    "Gender",
    "Date Of Birth",
    "Joined date",
  ];

  const keys = [
    "last_name",
    "first_name",
    "gender",
    "date_of_birth",
    "joined_date",
  ];

  return (
    <>
      {pageState === Page.ListStudent && (
        <div>
          <form className="row g-3 align-items-center pb-2">
            <div className="col-auto">
              <input
                type="text"
                className="form-control"
                id="first_name"
                placeholder="First Name"
              />
            </div>
            <div className="col-auto">
              <input
                type="text"
                className="form-control"
                id="last_name"
                placeholder="Last Name"
              />
            </div>
            <div className="col-auto btn-group">
              <button type="submit" className="btn btn-outline-primary">
                Search
              </button>
              <button
                type="submit"
                className="btn btn-outline-secondary"
                onClick={() => {
                  setStudentsState({
                    ...studentsState,
                    pageState: Page.AddStudent,
                  });
                }}
              >
                Add Student
              </button>
            </div>
          </form>
          <div className="table-responsive">
            <table className="table table-bordered table-hover table-striped">
              <caption>List of students</caption>
              <thead>
                <tr id="column_name">
                  <th></th>
                  {table_columns_names.map((colmunName) => {
                    return <th scope="col">{colmunName}</th>;
                  })}
                </tr>
              </thead>
              <tbody>
                {studentsState.value.map((student_info) => (
                  <tr>
                    <td>
                      <div className="centered">
                        <input type="radio" aria-label="Check for selection" />
                      </div>
                    </td>
                    {keys.map((column) => {
                      return <td> {student_info[column]}</td>;
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
      <hr className="hr pt-2" />
      {pageState === Page.AddStudent && (
        <AddStudents
          userAuth={userInfo.auth}
          updateStudentList={() => {
            fetchStudentLists();
          }}
        />
      )}
      {pageState === Page.RemoveStudent && (
        <RemoveStudents
          studentInfo={removeStudent.student}
          userAuth={userAuth}
          callBackUponSuccessRemoval={() => {
            updateStudentList();
          }}
          callBackUponExit={() => {
            setRemoveStudent({
              needRemoval: false,
              student: {},
            });
          }}
        />
      )}
    </>
  );
};

export default StudentsPage;
