import axios from "axios";

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
    .then(function (response) {
      if (response.data.calendar !== null) {
        var schoolDays: CalendarDate[] = [];
        response.data.calendar.forEach((day) => {
          let calendarDay: CalendarDate = JSON.parse(day);
          calendarDay.date = new Date(calendarDay.date);
          schoolDays.push(calendarDay);
        });
        callback({
          errMsg: "",
          calendar: schoolDays,
        });
      } else {
        callback({
          errMsg: "No calendar is found in the response!",
          calendar: [],
        });
      }
    })
    .catch(function (error) {
      if (error.response !== null) {
        callback({
          errMsg: error.response.data,
          calendar: [],
        });
      }
    });
};
