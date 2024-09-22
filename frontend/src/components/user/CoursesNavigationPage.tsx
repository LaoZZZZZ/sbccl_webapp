import React, { useEffect, useState } from "react";

import { RosterStudent, FetchCourseRoster } from "./FetchStudents.tsx";
import { fetchCourses, CourseList } from "./FetchCourses.tsx";
import { Auth, UserDetails } from "./UserInfo.tsx";
import RosterDetails from "../common/RosterDetails.tsx";
import { CourseInfo } from "../common/CourseInfo.tsx";
import Volunteers from "../common/Volunteers.tsx";
import CourseDropList from "../common/CourseDropList.tsx";
import { FetchVolunteers } from "../common/FetchVolunteers.tsx";

// #region component
interface CoursesNavigationPageProps {
  userAuth: Auth;
}

interface Roster {
  fetched: boolean;
  students: RosterStudent[];
}

interface Volunteers {
  fetched: boolean;
  volunteers: UserDetails[];
}

const ActiveTab = {
  ClassInformation: 0,
  Roster: 1,
  TeachingAssistant: 2,
};
/**
 *
 */
const CoursesNavigationPage = ({
  userAuth,
}: CoursesNavigationPageProps): JSX.Element => {
  // TODO(luzhao): Fetch the school info from the backend.
  const schoolYears = ["2024-2025"];
  const [selectedYear, setSelectedYear] = useState("2024-2025");
  const [courseState, setCourseState] = useState<CourseList>({
    fetched: false,
    courses: [],
  });

  const [activePage, setActivePage] = useState(ActiveTab.ClassInformation);
  const [roster, setRoster] = useState<Roster>({
    fetched: false,
    students: [],
  });

  const [selectedCourse, setSelectedCourse] = useState({
    selected: false,
    course: {},
  });

  const [volunteers, setVolunteers] = useState<Volunteers>({
    fetched: false,
    volunteers: [],
  });

  const handleFetchResponse = (response) => {
    setCourseState(response);
  };

  const handleRosterResponse = (roster: Roster) => {
    setRoster(roster);
  };
  const handleVolunteersResponse = (volunteers: Volunteers) => {
    setVolunteers(volunteers);
  };
  useEffect(() => {
    if (selectedYear.length > 0 && !courseState.fetched) {
      const school_year = selectedYear.split("-");
      fetchCourses(
        userAuth,
        school_year[0],
        school_year[1],
        handleFetchResponse
      );
    }
    if (selectedCourse.selected) {
      if (!roster.fetched) {
        FetchCourseRoster(
          userAuth,
          selectedCourse.course.id,
          handleRosterResponse
        );
      }
      if (!volunteers.fetched) {
        FetchVolunteers(
          userAuth,
          selectedCourse.course.id,
          handleVolunteersResponse
        );
      }
    }
  }, [courseState, roster, selectedCourse]);

  return (
    <div>
      <form className="pb-2">
        <div className="form row">
          <div className="col">
            <label>
              <strong>Select School year</strong>
            </label>
            <select
              className="form-control"
              id="selectYear"
              onChange={(e) => {
                if (selectedYear === e.target.value) {
                  return;
                }
                setSelectedYear(e.target.value);
                setCourseState({
                  fetched: false,
                  courses: [],
                });
              }}
            >
              {schoolYears.map((year) => {
                return <option>{year}</option>;
              })}
            </select>
          </div>
          <div className="col">
            <CourseDropList
              courses={courseState.fetched ? courseState.courses : []}
              retrieveCourseCallback={(selected) => {
                if (selected == null) {
                  setSelectedCourse({
                    selected: false,
                    course: {},
                  });
                } else {
                  setSelectedCourse({ selected: true, course: selected });
                  setRoster({
                    fetched: false,
                    students: [],
                  });
                  setVolunteers({
                    fetched: false,
                    volunteers: [],
                  });
                }
              }}
            />
          </div>
          {selectedCourse.selected && (
            <div className="btn-group pt-2">
              <input
                className={
                  "btn btn-outline-primary mr-3" +
                  (activePage === ActiveTab.ClassInformation ? " active" : "")
                }
                type="button"
                value="Class Information"
                onClick={() => {
                  setActivePage(ActiveTab.ClassInformation);
                }}
              />
              <input
                className={
                  "btn btn-outline-primary mr-3" +
                  (activePage === ActiveTab.Roster ? " active" : "")
                }
                type="button"
                value="Roster"
                onClick={() => {
                  setActivePage(ActiveTab.Roster);
                }}
              />
              <input
                className={
                  "btn btn-outline-primary mr-3" +
                  (activePage === ActiveTab.TeachingAssistant ? " active" : "")
                }
                type="button"
                value="Teaching Assistants"
                onClick={() => {
                  setActivePage(ActiveTab.TeachingAssistant);
                }}
              />
            </div>
          )}
        </div>
      </form>
      <hr className="pb-2" />

      {/* {selectedCourse.selected && (
        <div className="pt-2">
          <div className="container text-center pb-2">
            <h1>{getShownName(selectedCourse.course)}</h1>
          </div>
          <hr className="pb-2" />
        </div>
      )} */}
      {selectedCourse.selected && activePage === ActiveTab.ClassInformation && (
        <CourseInfo classInfo={selectedCourse.course} />
      )}
      {selectedCourse.selected && activePage === ActiveTab.Roster && (
        <RosterDetails
          students={roster.students}
          course={selectedCourse.course}
        />
      )}
      {selectedCourse.selected &&
        volunteers.fetched &&
        activePage === ActiveTab.TeachingAssistant && (
          <Volunteers volunteers={volunteers.volunteers} />
        )}
    </div>
  );
};
// #endregion

export default CoursesNavigationPage;
