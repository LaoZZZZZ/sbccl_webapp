import React, { useContext } from "react";
// import axios from "axios";

import { UserContext } from "../app/App.tsx";

// const userLogout = async (user_state) => {
//   await axios
//     .put("http://localhost:8000/rest_api/members/logout", {
//       user_state,
//     })
//     .then(function (response) {
//       console.log(response);
//       return {
//         page: Page.StartLogin,
//       };
//     });
// };

// Main page for user profile after login.
// Contains the following components:
// 1. User profile
// 2. Students under this user
// 3. Registrations associated with each student
const UserMainPage = () => {
  const [user_profile, transition] = useContext(UserContext);

  return <div>Hello, {JSON.stringify(user_profile.user_info)}</div>;
};

export default UserMainPage;
