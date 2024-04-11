import React from "react";
import { useState } from "react";

export interface ClassInformation {
  selected: boolean;
  enrollment: number;
  capacity: number;
  teacher: string;
  cost: string;
  type: string;
  classroom: string;
}

interface Props {
  courses: ClassInformation[];
  defaultCourseSelection: "";
  defaultPoDSelection: "";
  setCourseSelection: () => {};
  setPoDSelection: () => {};
}

//
const findSelectedCourse = (courses, value) => {
  const selected_course = courses.filter((course) => value === course.name);
  if (selected_course.length === 1) {
    return selected_course[0];
  }
  return null;
};

const CourseSelection = ({
  courses,
  defaultCourseSelection,
  defaultPoDSelection,
  setCourseSelection,
  setPoDSelection,
}: Props) => {
  // TODO(lu): Read the available dates from the backend.
  const podDates = [
    "2024-01-24 10:00am",
    "2024-01-24 01:00pm",
    "2024-02-24 10:00am",
    "2024-02-24 01:00pm",
    "2024-03-24 10:00am",
    "2024-04-24 10:00am",
    "2024-05-24 10:00am",
    "2024-06-24 10:00am",
    "2024-07-24 10:00am",
  ];

  const selectedCourse = findSelectedCourse(courses, defaultCourseSelection);
  const [classInfo, setClassInfo] = useState<ClassInformation>({
    selected: selectedCourse !== null,
    enrollment: selectedCourse !== null ? selectedCourse.enrollment : 0,
    capacity: selectedCourse !== null ? selectedCourse.size_limit : 0,
    teacher: "NA",
    cost: selectedCourse !== null ? "$" + selectedCourse.cost : "NA",
    type: selectedCourse !== null ? selectedCourse.course_type : "",
    classroom: selectedCourse !== null ? selectedCourse.classroom : "NA",
  });
  return (
    <>
      <div className="form-group">
        <label>
          <strong>Select class</strong>
        </label>
        <select
          className="form-control"
          id="selectCourse"
          onChange={(e) => {
            const selected_course = findSelectedCourse(courses, e.target.value);

            if (selected_course !== null) {
              console.log(selected_course);
              setCourseSelection(selected_course);
              setClassInfo({
                selected: true,
                enrollment: selected_course.enrollment,
                capacity: selected_course.size_limit,
                cost: "$" + selected_course.cost,
                type: selected_course.course_type,
                classroom: selected_course.classroom,
                teacher: "NA",
              });
            } else {
              setClassInfo({
                selected: false,
                enrollment: 0,
                capacity: 0,
                type: "",
                cost: "$0",
                classroom: "NA",
                teacher: "NA",
              });
            }
          }}
        >
          <option>{defaultCourseSelection}</option>
          {courses
            .filter((course) => {
              return course.name !== defaultCourseSelection;
            })
            .map((course) => {
              return <option>{course.name}</option>;
            })}
        </select>
      </div>
      {classInfo.selected && (
        <div className="input-group pb-2">
          <span className="input-group-text">Capacity:</span>
          <span className="input-group-text bg-white">
            {classInfo.capacity}
          </span>
          <span className="input-group-text">Enrollment:</span>
          <span
            className={
              "input-group-text " +
              (classInfo.enrollment >= classInfo.capacity
                ? "bg-danger"
                : "bg-white")
            }
          >
            {classInfo.enrollment}
          </span>
          <span className="input-group-text">Cost</span>
          <span className="input-group-text bg-white">{classInfo.cost}</span>
          <span className="input-group-text">Teacher</span>
          <span className="input-group-text bg-white">{classInfo.teacher}</span>
          <span className="input-group-text">Classroom</span>
          <span className="input-group-text bg-white">
            {classInfo.classroom}
          </span>
        </div>
      )}
      {/* TODO(lu): Bring it back once the PoD workflow is figured out. 
        {classInfo.selected && classInfo.type === "L" && (
        <div className="form-group pb-2">
          <label>Select Parent On Duty date</label>
          <select
            className="form-control"
            id="podSelect"
            onChange={(e) => {
              setPoDSelection(e.target.value);
            }}
          >
            <option>{defaultPoDSelection}</option>
            {podDates.map((date) => {
              return <option>{date}</option>;
            })}
          </select>
        </div>
      )} */}
    </>
  );
};

export default CourseSelection;
