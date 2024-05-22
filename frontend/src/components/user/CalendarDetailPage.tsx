import React, { useEffect, useState } from "react";
import {
  FetchCalendar,
  FetchResponse,
  CalendarDate,
} from "../common/FetchCalendar.tsx";
import Calendar from "../common/Calendar.tsx";

interface CalendarDetailPageProps {
  userAuth: {};
}

interface AcademicYearCalendar {
  schoolYear: string;
  calendar: CalendarDate[];
}

const generatePerYearCalendar = (allCalendar: FetchResponse) => {
  const result = new Map();
  allCalendar.calendar.forEach((day) => {
    const key = day.school_year_start + "-" + day.school_year_end;
    if (result.has(key)) {
      result.get(key).push(day);
    } else {
      result.set(key, [day]);
    }
  });
  var perYarCalendar: AcademicYearCalendar[] = [];
  result.forEach((v, k) => {
    perYarCalendar.push({
      schoolYear: k,
      calendar: v,
    });
  });
  return perYarCalendar;
};
/**
 *
 */
const CalendarDetailPage = ({ userAuth }: CalendarDetailPageProps) => {
  const [fetched, setFetched] = useState(false);

  const [perYearCalendar, setPerYearCalendar] = useState<
    AcademicYearCalendar[]
  >([]);

  const [selectedYear, setSelectedYear] = useState({
    selected: false,
    schoolDates: {},
  });

  const handleFetchResponse = (response: FetchResponse) => {
    const allyears = generatePerYearCalendar(response);
    setPerYearCalendar(allyears);
    if (allyears.length > 0) {
      setFetched(true);
    }
  };

  useEffect(() => {
    if (!fetched) {
      FetchCalendar(userAuth, handleFetchResponse);
    }
  }, [fetched]);

  return (
    <div>
      <div className="dropdown">
        <button
          className="btn btn-primary dropdown-toggle"
          type="button"
          id="dropdownMenuButton1"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          Choose School Year
        </button>
        <ul className="dropdown-menu" aria-labelledby="dropdownMenuButton1">
          {perYearCalendar.map((day: AcademicYearCalendar) => {
            return (
              <li>
                <button
                  className="dropdown-item"
                  onClick={() => {
                    setSelectedYear({ selected: true, schoolDates: day });
                  }}
                >
                  {day.schoolYear}
                </button>
              </li>
            );
          })}
        </ul>
      </div>
      {fetched && selectedYear.selected && (
        <Calendar
          schoolYear={selectedYear.schoolDates.schoolYear}
          schoolDates={selectedYear.schoolDates.calendar}
        />
      )}
    </div>
  );
};
// #endregion

export default CalendarDetailPage;
