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
      {!removeStudent.needRemoval && (
        <div className="table-responsive">
          <table className="table table-bordered table-hover table-striped">
            <caption>List of students</caption>
            <thead>
              <tr id="column_name">
                {table_columns_names.map((colmunName) => {
                  return <th scope="col">{colmunName}</th>;
                })}
                <th>#</th>
              </tr>
            </thead>
            <tbody>
              {students.map((student_info) => (
                <tr>
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
        <div>
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
        </div>
      )}
    </>
  );
};

export default ListStudents;
