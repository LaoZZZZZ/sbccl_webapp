import React from "react";
import { UserDetails } from "../user/UserInfo";

type Props = {
  volunteers: UserDetails[];
};

export default function Volunteers({ volunteers }: Props) {
  const table_columns_names = [
    "First name",
    "Last name",
    "Email",
    "Phone number",
  ];
  return (
    <div className="container text-center pb-2">
      <label>
        <strong>Volunteers</strong>
      </label>
      <div className="table-responsive">
        <table className="table table-bordered table-hover table-striped">
          <caption>List of volunteers</caption>
          <thead>
            <tr id="column_name">
              {table_columns_names.map((colmunName) => {
                return <th scope="col">{colmunName}</th>;
              })}
            </tr>
          </thead>

          <tbody>
            {volunteers.map((volunteer: UserDetails) => (
              <tr>
                <td>{volunteer.first_name}</td>
                <td>{volunteer.last_name}</td>
                <td>{volunteer.email}</td>
                <td>{volunteer.phone_number}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
  return <div>{volunteers.length}</div>;
}
