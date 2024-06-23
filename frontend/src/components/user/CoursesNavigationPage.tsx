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
        </div>
      </form>
      {roster.fetched && selectedCourse.selected && (
        <div className="pt-2">
          <div className="container text-center pb-2">
            <h1>{getShownName(selectedCourse.course)}</h1>
          </div>
          <hr className="pb-2" />

          <CourseInfo classInfo={selectedCourse.course} />
          <hr className="pb-2" />

          <RosterDetails
            students={roster.students}
            course={selectedCourse.course}
          />
        </div>
      )}
    </div>
  );
};
// #endregion

export default CoursesNavigationPage;
