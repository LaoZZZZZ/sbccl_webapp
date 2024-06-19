import React from "react";
import { ClassInformation, extractCourseTime } from "../user/FetchCourses.tsx";

// #region constants

// #endregion

// #region styled-components

// #endregion

// #region functions

// #endregion

// #region component

interface CourseInfoProps {
  classInfo: ClassInformation;
}

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
        <div className="card body text-start">
          {classInfo.course_description}
        </div>
      </div>
      <div className="card">
        <div className="row">
          <div className="col-4 text-wrap">
            <span className="input-group-text bg-info">Time</span>
            <span className="input-group-text bg-white">
              {extractCourseTime(classInfo)}
            </span>
          </div>
          <div className="col-4 text-wrap">
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
              {classInfo.size_limit}
            </span>
          </div>
          <div className="col-4">
            <span className="input-group-text bg-info">Enrollment:</span>
            <span
              className={
                "input-group-text " +
                (classInfo.enrollment >= classInfo.size_limit
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
