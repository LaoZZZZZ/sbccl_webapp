import React from "react";
import { RosterStudent } from "../user/FetchStudents.tsx";
import { ClassInformation, getShownName } from "../user/FetchCourses.tsx";

interface Props {
  students: RosterStudent[];
  course: ClassInformation;
}

const onWaitingList = [true, false];
const legends = new Map([
  [true, "OnWaitingList"],
  [false, "Enrolled"],
]);

const colors = new Map([
  [true, "text-warning"],
  [false, "text-success"],
]);

const getBackgroundColor = (student: RosterStudent) => {
  return colors.get(student.on_waiting_list);
};

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
      <div className="pb-2">
        {onWaitingList.map((status: boolean) => (
          <span className={"badge " + colors.get(status)}>
            {legends.get(status)}
          </span>
        ))}
      </div>
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
                <td className={getBackgroundColor(student_info)}>
                  {student_info.last_name}
                </td>
                <td className={getBackgroundColor(student_info)}>
                  {student_info.first_name}
                </td>
                <td className={getBackgroundColor(student_info)}>
                  {student_info.chinese_name}
                </td>
                <td className={getBackgroundColor(student_info)}>
                  {student_info.gender}
                </td>
                <td className={getBackgroundColor(student_info)}>
                  {student_info.age}
                </td>
                <td className={getBackgroundColor(student_info)}>
                  {student_info.contact.parent}
                </td>
                <td className={getBackgroundColor(student_info)}>
                  {student_info.contact.email}
                </td>
                <td className={getBackgroundColor(student_info)}>
                  {student_info.contact.phone}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
