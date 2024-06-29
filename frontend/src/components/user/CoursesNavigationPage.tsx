import React, { useEffect, useState } from "react";

import { RosterStudent, FetchCourseRoster } from "./FetchStudents.tsx";
import fetchCourses, {
  ClassInformation,
  findSelectedCourse,
  getShownName,
} from "./FetchCourses.tsx";
import { Auth } from "./UserInfo.tsx";
import RosterDetails from "../common/RosterDetails.tsx";
import { CourseInfo } from "../common/CourseInfo.tsx";
import Volunteers from "../common/Volunteers.tsx";

// #region component
interface CoursesNavigationPageProps {
  userAuth: Auth;
}

interface Roster {
  fetched: boolean;
  students: RosterStudent[];
}

interface CourseList {
  fetched: boolean;
  courses: ClassInformation[];
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
  const [selectedYear, setSelectedYear] = useState("");
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

  const handleFetchResponse = (response) => {
    setCourseState(response);
  };

  const handleRosterResponse = (roster: Roster) => {
    setRoster(roster);
  };
  useEffect(() => {
    if (!courseState.fetched) {
      fetchCourses(userAuth, handleFetchResponse);
    }
    if (selectedCourse.selected && !roster.fetched) {
      FetchCourseRoster(
        userAuth,
        selectedCourse.course.id,
        handleRosterResponse
      );
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
            <div>
              <label>
                <strong>Select course</strong>
              </label>
              <select
                className="form-control"
                id="selectCourse"
                onChange={(e) => {
                  if (e.target.value === "Not Selected") {
                    setSelectedCourse({
                      selected: false,
                      course: {},
                    });
                    return;
                  }
                  if (
                    selectedCourse.selected &&
                    selectedCourse.course.name === e.target.value
                  ) {
                    return;
                  }
                  const new_selected = findSelectedCourse(
                    courseState.courses,
                    e.target.value
                  );

                  setSelectedCourse({ selected: true, course: new_selected });
                  setRoster({
                    fetched: false,
                    students: [],
                  });
                }}
              >
                <option>Not Selected</option>
                {courseState.fetched &&
                  courseState.courses.map((course: ClassInformation) => {
                    return <option>{getShownName(course)}</option>;
                  })}
              </select>
            </div>
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
        activePage === ActiveTab.TeachingAssistant && <Volunteers />}
    </div>
  );
};
// #endregion

export default CoursesNavigationPage;
