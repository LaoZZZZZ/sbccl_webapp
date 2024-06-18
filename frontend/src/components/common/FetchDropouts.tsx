import axios from "axios";
import { Student } from "../user/FetchStudents";

export interface Dropout {
  id: number;
  course_name: string;
  student: number;
  school_year_start: Date;
  school_year_end: Date;
  original_registration_code: string;
}

export interface DropoutBundle {
  student: Student;
  dropout: Dropout;
  balance: number;
}

export interface Dropouts {
  errMsg: string;
  dropouts: DropoutBundle[];
}
/**
 *
 * @param user_auth: user authentication information for api call
 * @param callback: Client provided callback upon receiving response.
 * @returns
 */
export const FetchDropouts = async (user_auth: {}, callback) => {
  await axios
    .get(
      process.env.REACT_APP_BE_URL_PREFIX + "/rest_api/members/list-dropouts/",
      {
        headers: {
          "Content-Type": "application/json",
        },
        auth: user_auth,
      }
    )
    .then((response) => {
      callback({
        fetched: true,
        value: response.data.dropouts.map(JSON.parse),
      });
    })
    .catch((error) => {
      callback({
        errMsg: error.response.data.detail,
        value: null,
      });
    });
};
