import React from "react";

// #region constants

// #endregion

// #region styled-components

// #endregion

// #region functions

// #endregion

// #region component
export interface SchoolDate {
  event: string;
  date: Date;
  school_year_start: Date;
  school_year_end: Date;
}
interface CalendarProps {
  schoolDates: SchoolDate[];
}

const processSchoolDates = (schoolDates: SchoolDate[]) => {
  schoolDates.sort((a, b) => a.date.getTime() - b.date.getTime());
  const today = new Date();
  today.setHours(16);
  var past_date: SchoolDate[] = [];
  var future_dates: SchoolDate[] = [];
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
export const Calendar = ({ schoolDates }: CalendarProps) => {
  const hasSchool = schoolDates.length > 0;
  const calendar = processSchoolDates(schoolDates);
  const table_columns_names = ["Date", "Event"];
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
            <h1>Calendar</h1>
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
                {calendar.future.map((day: SchoolDate) => (
                  <tr>
                    <td>{day.date.toDateString()}</td>
                    <td>{day.event}</td>
                  </tr>
                ))}
                <tr className="table-light">
                  <th colspan="2"> Past Events</th>
                </tr>
                {calendar.past.map((day: SchoolDate) => (
                  <tr className="table-secondary">
                    <td>{day.date.toDateString()}</td>
                    <td>{day.event}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
// #endregion

export default Calendar;
