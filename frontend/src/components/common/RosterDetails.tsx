import React from "react";
import { RosterStudent } from "../user/FetchStudents.tsx";
import { ClassInformation, getShownName } from "../user/FetchCourses.tsx";

interface Props {
  students: RosterStudent[];
  course: ClassInformation;
}

export default function RosterDetails({ students, course }: Props) {
  const table_columns_names = [
    "Last Name",
    "First Name",
    "Chinese Name",
    "Gender",
    "Age",
    "Parent",
    "Email",
    "Phone",
  ];

  return (
    <div className="container text-center pb-2">
      <label>
        <strong>Roster</strong>
      </label>
      <div className="table-responsive">
        <table className="table table-bordered table-hover table-striped">
          <caption>List of students</caption>
          <thead>
            <tr id="column_name">
              {table_columns_names.map((colmunName) => {
                return <th scope="col">{colmunName}</th>;
              })}
            </tr>
          </thead>
          <tbody>
            {students.map((student_info: RosterStudent) => (
              <tr>
                <td>{student_info.last_name}</td>
                <td>{student_info.first_name}</td>
                <td>{student_info.chinese_name}</td>
                <td>{student_info.gender}</td>
                <td>{student_info.age}</td>
                <td>{student_info.contact.parent}</td>
                <td>{student_info.contact.email}</td>
                <td>{student_info.contact.phone}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
