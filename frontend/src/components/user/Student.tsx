import React from "react";

interface Props {
  student: {};
  columns: [];
}

const Student = ({ student, columns }: Props) => {
  console.log(student);
  return (
    <tr>
      {columns.map((key) => {
        return <td> {student[key]}</td>;
      })}
      <td>
        <div className="dropend">
          <button
            className="btn btn-primary dropdown-toggle"
            type="button"
            data-bs-toggle="dropdown"
            aria-expanded="false"
          >
            Update
          </button>
          <ul className="dropdown-menu">
            <li>
              <a className="dropdown-item" href="#">
                Action
              </a>
            </li>
            <li>
              <a className="dropdown-item" href="#">
                Another action
              </a>
            </li>
            <li>
              <a className="dropdown-item" href="#">
                Something else here
              </a>
            </li>
          </ul>
        </div>
      </td>
    </tr>
  );
};

export default Student;
