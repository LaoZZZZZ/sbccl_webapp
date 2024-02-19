import React from "react";

interface Props {
  userInfo: {};
}

const AccountDetail = ({ userInfo }: Props) => {
  console.log(userInfo);
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
      <table className="table table-bordered table-hover">
        <tbody>
          {table_row_names.map((key_value) => {
            return (
              <tr>
                <th>
                  <strong>{key_value.rowName}</strong>
                </th>
                <th>{key_value.value}</th>
              </tr>
            );
          })}
        </tbody>
      </table>
      <div></div>
    </>
  );
};

export default AccountDetail;
