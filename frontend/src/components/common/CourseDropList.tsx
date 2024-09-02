import React, { useState } from "react";
import { ClassInformation, getShownName } from "../user/FetchCourses.tsx";

interface Props {
  courses: ClassInformation[];
  retrieveCourseCallback: (selected: ClassInformation) => void;
}

// Find course in courses that is suffix of the course name shown on the screen.
// @courseName: It's the name shown on the screen, and might be different from the actual name
export const findSelectedCourse = (courses, courseName) => {
  const selected_course = courses.filter((course) =>
    courseName.endsWith(course.name)
  );
  if (selected_course.length === 1) {
    return selected_course[0];
  }
  return null;
};

export default function CourseDropList({
  courses,
  retrieveCourseCallback,
}: Props) {
  const [selectedCourse, setSelectedCourse] = useState({
    selected: false,
    course: {},
  });
  return (
    <div>
      <label>
        <strong>Select class</strong>
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
            retrieveCourseCallback(null);
            return;
          }
          if (
            selectedCourse.selected &&
            selectedCourse.course.name === e.target.value
          ) {
            return;
          }
          const new_selected = findSelectedCourse(courses, e.target.value);
          setSelectedCourse({
            selected: true,
            course: new_selected,
          });
          retrieveCourseCallback(new_selected);
        }}
      >
        <option>Not Selected</option>
        {courses.length > 0 &&
          courses.map((course: ClassInformation) => {
            return <option>{getShownName(course)}</option>;
          })}
      </select>
    </div>
  );
}
