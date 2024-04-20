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
  course_start: string;
  course_end: string;
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
    teacher: selectedCourse != null ? selectedCourse.teacher : "NA",
    cost: selectedCourse !== null ? "$" + selectedCourse.cost : "NA",
    type: selectedCourse !== null ? selectedCourse.course_type : "",
    classroom: selectedCourse !== null ? selectedCourse.classroom : "NA",
    course_start:
      selectedCourse !== null ? selectedCourse.course_start_time : "NA",
    course_end: selectedCourse !== null ? selectedCourse.course_end_time : "NA",
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
              setCourseSelection(selected_course);
              setClassInfo({
                selected: true,
                enrollment: selected_course.enrollment,
                capacity: selected_course.size_limit,
                cost: "$" + selected_course.cost,
                type: selected_course.course_type,
                classroom: selected_course.classroom,
                teacher: selected_course.teacher,
                course_start: selected_course.course_start_time,
                course_end: selected_course.course_end_time,
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
                course_start: "NA",
                course_end: "NA",
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
          <span className="input-group-text bg-info">Capacity:</span>
          <span className="input-group-text bg-white">
            {classInfo.capacity}
          </span>
          <span className="input-group-text bg-info">Enrollment:</span>
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
          <span className="input-group-text bg-info">Cost</span>
          <span className="input-group-text bg-white">{classInfo.cost}</span>
          <span className="input-group-text bg-info">Teacher</span>
          <span className="input-group-text bg-white">{classInfo.teacher}</span>
          <span className="input-group-text bg-info">Classroom</span>
          <span className="input-group-text bg-white">
            {classInfo.classroom}
          </span>
          <span className="input-group-text">Time</span>
          <span className="input-group-text bg-white">
            {classInfo.course_start + " - " + classInfo.course_end}
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
