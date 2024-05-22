import axios from "axios";
import { json } from "stream/consumers";

export interface CalendarDate {
  date: Date;
  event: string;
  day_type: string;
  school_year_start: number;
  school_year_end: number;
}

export interface FetchResponse {
  errMsg: string;
  calendar: CalendarDate[];
}

// #endregion

/**
 *
 * @param user_auth: user authentication information for api call
 * @param callback:
 * @returns
 */
export const FetchCalendar = async (
  user_auth: {},
  callback: (response: FetchResponse) => {}
) => {
  await axios
    .get(
      process.env.REACT_APP_BE_URL_PREFIX + "/rest_api/members/fetch-calendar/",
      {
        headers: {
          "Content-Type": "application/json",
        },
        auth: user_auth,
      }
    )
    .then((response) => {
      if (response.data.calendar !== null) {
        var calendar: CalendarDate[] = [];
        response.data.calendar.forEach((day) => {
          calendar.push(day);
        });
        callback({
          errMsg: "",
          calendar: calendar,
        });
      } else {
        callback({
          errMsg: "No calendar is found in the response!",
          calendar: [],
        });
      }
      return;
    })
    .catch((error) => {
      callback({
        errMsg: error.response.data.detail,
        calendar: [],
      });
    });
};
