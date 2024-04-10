import React, { useEffect, useState } from "react";

import fetchAccountDetails from "./FetchAccountDetails.tsx";
interface Props {
  userInfo: {};
}

interface UserState {
  fetched: boolean;
  value: {};
}

const AccountDetail = ({ userInfo }: Props) => {
  const [userState, setUserState] = useState<UserState>({
    fetched: false,
    value: userInfo.user,
  });

  useEffect(() => {
    if (!userState.fetched) {
      fetchAccountDetails(userInfo.auth, setUserState);
    }
  }, [userState]);

  // const table_row_names = [
  //   { rowName: "Last Name", value: userInfo.user.last_name },
  //   { rowName: "First Name", value: userInfo.user.first_name },
  //   { rowName: "Email", value: userInfo.user.email },
  //   { rowName: "Phone Number", value: userInfo.user.phone_number },
  //   { rowName: "Member Type", value: userInfo.user.member_type },
  //   { rowName: "Last Login", value: userInfo.user.last_login },
  //   { rowName: "Date Joined", value: userInfo.user.date_joined },
  //   { rowName: "Balance", value: userInfo.user.balance },
  // ];

  // TODO(lu): Make phone number editable for the user.
  return (
    <>
      {userState.fetched && (
        <table className="table table-bordered table-hover" id="AccountDetails">
          <tbody>
            <tr id="last_name">
              <th>Last Name</th>
              <td>{userState.value.last_name}</td>
            </tr>
            <tr id="first_name">
              <th>First Name</th>
              <td>{userState.value.first_name}</td>
            </tr>
            <tr id="email">
              <th>Email</th>
              <td>{userState.value.email}</td>
            </tr>
            <tr id="phone_number">
              <th>Phone Number</th>
              <td>{userState.value.phone_number}</td>
            </tr>
            <tr id="member_type">
              <th>Member Type</th>
              <td>{userState.value.member_type}</td>
            </tr>
            <tr id="last_login">
              <th>Last Login</th>
              <td>{userState.value.last_login}</td>
            </tr>
            <tr id="date_joined">
              <th>Date Joined</th>
              <td>{userState.value.date_joined}</td>
            </tr>
            <tr id="balance">
              <th>Balance</th>
              <td>{userState.value.balance}</td>
            </tr>
            {/* {table_row_names.map((key_value) => {
              return (
                <tr id={key_value.rowName}>
                  <th>{key_value.rowName}</th>
                  <td>{key_value.value}</td>
                </tr>
              );
            })} */}
          </tbody>
        </table>
      )}
    </>
  );
};

export default AccountDetail;
