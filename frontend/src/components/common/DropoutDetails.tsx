import React from "react";
import { DropoutBundle, Dropout } from "./FetchDropouts";

// #region component
interface DropoutDetailsProps {
  dropouts: DropoutBundle[];
}

/**
 *
 */
const DropoutDetails = ({ dropouts }: DropoutDetailsProps): JSX.Element => {
  const table_columns_names = [
    "Student",
    "Course",
    "School Year",
    "Status",
    "Balance",
  ];

  return (
    <div>
      {dropouts.length > 0 && (
        <div className="table-responsive">
          <table className="table table-bordered table-hover table-striped">
            <caption>List of Dropouts</caption>
            <thead>
              <tr id="column_name">
                {table_columns_names.map((colmunName) => {
                  return <th scope="col">{colmunName}</th>;
                })}
              </tr>
            </thead>
            <tbody>
              {dropouts.map((bundle: DropoutBundle) => (
                <tr>
                  <td>
                    {bundle.student.first_name + " " + bundle.student.last_name}
                  </td>
                  <td>{bundle.dropout.course_name}</td>
                  <td>
                    {new Date(bundle.dropout.school_year_start).getFullYear() +
                      "-" +
                      new Date(bundle.dropout.school_year_end).getFullYear()}
                  </td>
                  <td>
                    {bundle.balance === 0
                      ? "Withdraw completed"
                      : "Withdraw requested"}
                  </td>
                  <td>{"$" + bundle.balance.toString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
// #endregion

export default DropoutDetails;
