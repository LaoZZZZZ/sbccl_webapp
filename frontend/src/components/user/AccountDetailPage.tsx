import React from "react";

import fetchAccountDetails from "./FetchAccountDetails.tsx";
interface Props {
  userInfo: {};
}

const AccountDetail = ({ userInfo }: Props) => {
  const table_row_names = [
    { rowName: "Last Name", value: userInfo.last_name },
    { rowName: "First Name", value: userInfo.first_name },
    { rowName: "Email", value: userInfo.email },
    { rowName: "Phone Number", value: userInfo.phone_number },
    { rowName: "Member Type", value: userInfo.member_type },
    { rowName: "Last Login", value: userInfo.last_login },
    { rowName: "Date Joined", value: userInfo.date_joined },
    { rowName: "Balance", value: userInfo.balance },
  ];

  // TODO(lu): Make phone number editable for the user.
  return (
    <>
      <table className="table table-bordered table-hover" id="AccountDetails">
        <tbody>
          {table_row_names.map((key_value) => {
            return (
              <tr id={key_value.rowName}>
                <th>{key_value.rowName}</th>
                <td>{key_value.value}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </>
  );
};

export default AccountDetail;
