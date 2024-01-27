import React from "react";

interface Props {
  userInfo: {};
}

const AccountDetail = ({ userInfo }: Props) => {
  console.log(userInfo);
  const table_row_names = [
    { rowName: "Last Name", key: "last_name" },
    { rowName: "First Name", key: "first_name" },
    { rowName: "Email", key: "email" },
    { rowName: "Phone Number", key: "phone_number" },
    { rowName: "Member Type", key: "member_type" },
    { rowName: "Last Login", key: "last_login" },
    { rowName: "Date Joined", key: "date_joined" },
    { rowName: "Balance", key: "balance" },
  ];

  return (
    <table className="table table-bordered table-hover">
      <tbody>
        {table_row_names.map((key_value) => {
          return (
            <tr>
              <th>{key_value.rowName}</th>
              <th>{userInfo[key_value.key]}</th>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
};

export default AccountDetail;
