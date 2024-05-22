import React from "react";

import { CalendarDate } from "./FetchCalendar.tsx";
// #region constants

// #endregion

// #region styled-components

// #endregion

// #region functions

// #endregion

// #region component

interface CalendarProps {
  schoolYear: string;
  schoolDates: CalendarDate[];
}

const processSchoolDates = (schoolDates: CalendarDate[]) => {
  schoolDates.sort((a, b) => a.date.getTime() - b.date.getTime());
  const today = new Date();
  today.setHours(16);
  var past_date: CalendarDate[] = [];
  var future_dates: CalendarDate[] = [];
  schoolDates.forEach((schoolDate) => {
    if (schoolDate.date.getTime() < today.getTime()) {
      past_date.push(schoolDate);
    } else {
      future_dates.push(schoolDate);
    }
  });

  return {
    past: past_date,
    future: future_dates,
  };
};
/**
 *
 */
export const Calendar = ({ schoolYear, schoolDates }: CalendarProps) => {
  const hasSchool = schoolDates.length > 0;
  const calendar = processSchoolDates(schoolDates);
  const table_columns_names = ["Date", "Event"];
  const options = {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
    timeZone: "UTC",
  };

  return (
    <div>
      {!hasSchool && (
        <div className="container text-center pb-2">
          <h1>The current school year has ended!</h1>
        </div>
      )}
      {hasSchool && (
        <div className="container text-center pb-2">
          <div>
            <h1>{schoolYear}</h1>
          </div>
          <div className="table-responsive">
            <table className="table table-primary table-striped-columns">
              <thead>
                <tr id="column_name">
                  {table_columns_names.map((colmunName) => {
                    return <th scope="col">{colmunName}</th>;
                  })}
                </tr>
              </thead>
              <tbody>
                <tr className="table-primary">
                  <th colspan="2"> Future Events</th>
                </tr>
                {calendar.future.map((day: CalendarDate) => (
                  <tr>
                    <td
                      className={
                        day.day_type === "SD" ? "bg-success" : "bg-info"
                      }
                    >
                      {day.date.toLocaleDateString("en-US", options)}
                    </td>
                    <td>{day.event}</td>
                  </tr>
                ))}
                <tr className="table-light">
                  <th colspan="2"> Past Events</th>
                </tr>
                {calendar.past.map((day: CalendarDate) => (
                  <tr className="table-secondary">
                    <td>{day.date.toLocaleDateString("en-US", options)}</td>
                    <td>{day.event}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div>
            <span className="badge bg-success">School Day</span>
            <span className="badge bg-info">School Closed</span>
          </div>
        </div>
      )}
    </div>
  );
};
// #endregion

export default Calendar;
