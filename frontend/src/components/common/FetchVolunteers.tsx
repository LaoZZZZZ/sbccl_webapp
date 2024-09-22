import { Auth, UserDetails } from "../user/UserInfo";
import axios from "axios";

interface Props {
  auth: Auth;
  courseId: number;
  callback: (details: UserDetails) => {};
}

export const FetchVolunteers = async (
  auth: Auth,
  courseId: number,
  callback: ({}) => {}
) => {
  var url =
    process.env.REACT_APP_BE_URL_PREFIX +
    `/rest_api/members/${courseId}/list-volunteers-per-class`;

  const response = await axios.get(url, {
    headers: {
      "Content-Type": "application/json",
    },
    auth: {
      username: auth.username,
      password: auth.password,
    },
  });

  if (response.status === 200) {
    console.log(response.data);
    const volunteers = response.data.volunteers.map(JSON.parse);
    volunteers.sort((a: UserDetails, b: UserDetails) => {
      if (a.first_name < b.first_name) {
        return -1;
      } else if (a.first_name > b.first_name) {
        return 1;
      }
      return 0;
    });
    callback({
      fetched: true,
      volunteers: volunteers,
    });
    return;
  }

  callback({ fetched: true, volunteers: [] });
};
