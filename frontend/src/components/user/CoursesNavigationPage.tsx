import React, { useEffect, useState } from "react";

import { RosterStudent, FetchCourseRoster } from "./FetchStudents.tsx";
import fetchCourses, { ClassInformation } from "./FetchCourses.tsx";
import { Auth } from "./UserInfo.tsx";
import RosterDetails from "../common/RosterDetails.tsx";

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
    console.log(roster);
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
      <div className="dropdown">
        <button
          className="btn btn-primary dropdown-toggle"
          type="button"
          id="dropdownMenuButton1"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          Courses
        </button>
        <ul className="dropdown-menu" aria-labelledby="dropdownMenuButton1">
          {courseState.fetched &&
            courseState.courses.map((course: ClassInformation) => {
              return (
                <li>
                  <button
                    className="dropdown-item"
                    onClick={() => {
                      setSelectedCourse({ selected: true, course: course });
                      setRoster({
                        fetched: false,
                        students: [],
                      });
                    }}
                  >
                    {course.name}
                  </button>
                </li>
              );
            })}
        </ul>
      </div>
      {roster.fetched && selectedCourse.selected && (
        <RosterDetails
          students={roster.students}
          course={selectedCourse.course}
        />
      )}
    </div>
  );
};
// #endregion

export default CoursesNavigationPage;
