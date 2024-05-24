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

const generatePerYearCalendar = (response: FetchResponse) => {
  const result = new Map();
  response.calendar.forEach((schoolDay: CalendarDate) => {
    const key: string =
      schoolDay.school_year_start + "-" + schoolDay.school_year_end;

    if (result.has(key)) {
      result.get(key).push(schoolDay);
    } else {
      result.set(key, [schoolDay]);
    }
  });
  var perYarCalendar: AcademicYearCalendar[] = [];
  result.forEach((days, year) => {
    perYarCalendar.push({
      schoolYear: year,
      calendar: days,
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
    schoolDates: {
      schoolYear: "",
      calendar: [],
    },
  });

  const handleFetchResponse = (response: FetchResponse) => {
    const allyears = generatePerYearCalendar(response);
    setPerYearCalendar(allyears);
    if (allyears.length > 0) {
      setSelectedYear({
        selected: true,
        schoolDates: allyears[0],
      });
    }
    setFetched(allyears.length > 0);
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
                    console.log(day);
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
