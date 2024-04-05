import React, { useState } from "react";
import RemoveStudents from "./RemoveStudentsPage.tsx";

interface Props {
  students: [];
  userAuth: {};
  updateStudentList: () => {};
}

const ListStudents = ({ students, userAuth, updateStudentList }: Props) => {
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
          <button type="submit" className="btn btn-outline-secondary">
            Add Student
          </button>
        </div>
      </form>
      {!removeStudent.needRemoval && (
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
              {students.map((student_info) => (
                <tr>
                  <td>
                    <div className="centered">
                      <input type="radio" aria-label="Check for selection" />
                    </div>
                  </td>
                  {keys.map((column) => {
                    return <td> {student_info[column]}</td>;
                  })}
                  <td>
                    <button
                      className="btn btn-outline-secondary"
                      data-toggle="modal"
                      type="button"
                      onClick={(e) => {
                        setRemoveStudent({
                          needRemoval: true,
                          student: student_info,
                        });
                      }}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {removeStudent.needRemoval && (
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

export default ListStudents;
