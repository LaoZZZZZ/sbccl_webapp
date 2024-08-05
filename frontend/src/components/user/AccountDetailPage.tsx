import React, { useEffect, useState } from "react";

import { AccountInfo, UserDetails } from "./UserInfo.tsx";
import fetchAccountDetails from "./FetchAccountDetails.tsx";
interface Props {
  userInfo: AccountInfo;
}

interface UserState {
  fetched: boolean;
  value: UserDetails;
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
          </tbody>
        </table>
      )}
    </>
  );
};

export default AccountDetail;
