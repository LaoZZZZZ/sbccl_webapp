import React from "react";
import { RegistrationBundle } from "./FetchRegistrations";
import { Student } from "../user/FetchStudents";
// #region constants

// #endregion

// #region styled-components

// #endregion

// #region functions
const renderRegistration = (student: Student) => {
  return student.last_name + " " + student.last_name;
};
// #endregion

// #region component
interface RegistrationDetailsProps {
  registrations: RegistrationBundle[];
  showTeacherInfo: ({}) => {};
  editRegistration: (registration: RegistrationBundle) => {};
}

/**
 *
 */
const RegistrationDetails = ({
  registrations,
  showTeacherInfo,
  editRegistration,
}: RegistrationDetailsProps): JSX.Element => {
  const table_columns_names = [
    "Student",
    "Course",
    "School Year",
    "Status",
    "Balance",
    "Teacher",
  ];

  return (
    <>
      {registrations.length > 0 && (
        <div className="table-responsive">
          <table className="table table-bordered table-hover table-striped">
            <caption>List of registrations</caption>
            <thead>
              <tr id="column_name">
                {table_columns_names.map((colmunName) => {
                  return (
                    <th scope="col" className="bg-info">
                      {colmunName}
                    </th>
                  );
                })}
              </tr>
            </thead>
            <tbody>
              {registrations.map((r) => (
                <tr>
                  <td>
                    <button
                      className={"btn btn-outline-secondary"}
                      data-toggle="modal"
                      onClick={(e) => {
                        editRegistration(r);
                      }}
                    >
                      {renderRegistration(r.student)}
                    </button>
                  </td>
                  <td>{r.course.name}</td>
                  <td>
                    {new Date(r.registration.school_year_start).getFullYear() +
                      " - " +
                      new Date(r.registration.school_year_end).getFullYear()}
                  </td>
                  <td>
                    {r.registration.on_waiting_list
                      ? "On Waiting List"
                      : "Enrolled"}
                  </td>
                  <td>{"$" + r.balance.toString()}</td>
                  <td>
                    <button
                      className={"btn btn-outline-secondary"}
                      data-toggle="modal"
                      onClick={(e) => {
                        showTeacherInfo({
                          class_name: r.course.name,
                          teachers_info: r.teacher,
                        });
                      }}
                    >
                      Teacher information
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
};
// #endregion

export default RegistrationDetails;
