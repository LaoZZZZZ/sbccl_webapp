import React from "react";

// #region constants

// #endregion

// #region styled-components

// #endregion

// #region functions

// #endregion

// #region component
export interface ClassInformation {
  enrollment: number;
  capacity: number;
  teacher: string;
  cost: number;
  type: string;
  classroom: string;
  course_start: string;
  course_end: string;
  book_cost: number;
  course_description: string;
}

interface CourseInfoProps {
  classInfo: ClassInformation;
}

const extractCourseTime = (course: ClassInformation) => {
  var start = new Date("2024-10-01T" + course.course_start);
  var end = new Date("2024-10-01T" + course.course_end);
  return (
    start.toLocaleString("en-US", {
      hour: "numeric",
      hour12: true,
      minute: "numeric",
    }) +
    " - " +
    end.toLocaleString("en-US", {
      hour: "numeric",
      hour12: true,
      minute: "numeric",
    })
  );
};

/**
 * Render a class information.
 */
export const CourseInfo = ({ classInfo }: CourseInfoProps) => {
  return (
    <div className="container text-center pb-2">
      <label>
        <strong>Class Information</strong>
      </label>
      <div className="card">
        <div className="card body">{classInfo.course_description}</div>
      </div>
      <div className="card">
        <div className="row justify-content-start">
          <div className="col-4">
            <span className="input-group-text bg-info">Time</span>
            <span className="input-group-text bg-white">
              {extractCourseTime(classInfo)}
            </span>
          </div>
          <div className="col-4">
            <span className="input-group-text bg-info">Classroom</span>
            <span className="input-group-text bg-white">
              {classInfo.classroom}
            </span>
          </div>
          <div className="col-4">
            <span className="input-group-text bg-info">Tuition</span>
            <span className="input-group-text bg-white">${classInfo.cost}</span>
          </div>
          <div className="col-4">
            <span className="input-group-text bg-info">Capacity:</span>
            <span className="input-group-text bg-white">
              {classInfo.capacity}
            </span>
          </div>
          <div className="col-4">
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
          </div>
          <div className="col-4">
            <span className="input-group-text bg-info">Teacher</span>
            <span className="input-group-text bg-white">
              {classInfo.teacher}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
// #endregion