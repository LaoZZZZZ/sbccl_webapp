import React from "react";
import PageHead from "../common/PageHead.tsx";
import ListStudent from "./ListStudent.tsx";

interface Props {
  userInfo: React.ReactNode;
}

// Main page for user profile after login.
// Contains the following components:
// 1. User profile
// 2. Students under this user
// 3. Registrations associated with each student
const UserMainPage = ({ userInfo }: Props) => {
  console.log(userInfo);
  let users = ["abc", "def"];

  return (
    <>
      <PageHead />
      <ListStudent userInfo={userInfo} />
    </>
  );
};

export default UserMainPage;
