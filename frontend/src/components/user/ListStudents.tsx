import React, { useEffect, useState } from "react";
import axios from "axios";

interface Props {
  students: [];
}

const ListStudents = ({ students }: Props) => {
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
    <div className="table-responsive">
      <table className="table table-bordered table-hover table-striped">
        <caption>List of students</caption>
        <thead>
          <tr>
            {table_columns_names.map((colmunName) => {
              return <th scope="col">{colmunName}</th>;
            })}
            <th></th>
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
                  type="button"
                  onClick={() => {}}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ListStudents;
