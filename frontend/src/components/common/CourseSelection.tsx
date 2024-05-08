import React from "react";
import { useState } from "react";
import TotalCost from "./TotalCost.tsx";
import GetCoupon from "./GetCoupon.tsx";

export interface ClassInformation {
  enrollment: number;
  capacity: number;
  teacher: string;
  cost: number;
  type: string;
  classroom: string;
  course_start: string;
  course_end: string;
}

interface Props {
  user_auth: {};
  courses: ClassInformation[];
  defaultCourseSelection: "";
  defaultPoDSelection: "";
  setCourseSelection: () => {};
  populateCouponCode: (code: string) => {};
}

//
const findSelectedCourse = (courses, value) => {
  const selected_course = courses.filter((course) => value === course.name);
  if (selected_course.length === 1) {
    return selected_course[0];
  }
  return null;
};

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

const CourseSelection = ({
  user_auth,
  courses,
  defaultCourseSelection,
  setCourseSelection,
  populateCouponCode,
}: Props) => {
  const selectedCourse = findSelectedCourse(courses, defaultCourseSelection);
  const [selected, setSelected] = useState(selectedCourse !== null);

  const [classInfo, setClassInfo] = useState<ClassInformation>({
    enrollment: selectedCourse !== null ? selectedCourse.enrollment : 0,
    capacity: selectedCourse !== null ? selectedCourse.size_limit : 0,
    teacher: selectedCourse != null ? selectedCourse.teacher : "NA",
    cost: selectedCourse !== null ? selectedCourse.cost : 0,
    type: selectedCourse !== null ? selectedCourse.course_type : "",
    classroom: selectedCourse !== null ? selectedCourse.classroom : "NA",
    course_start:
      selectedCourse !== null ? selectedCourse.course_start_time : "NA",
    course_end: selectedCourse !== null ? selectedCourse.course_end_time : "NA",
  });
  const [waitForResponse, setWaitForResponse] = useState(false);
  const [cost, setCost] = useState(classInfo.cost);

  const [couponCode, setCouponCode] = useState("");
  const [couponApplied, setCouponApplied] = useState(false);
  return (
    <>
      <div className="form-group pb-2">
        <label>
          <strong>Select class</strong>
        </label>
        <select
          className="form-control"
          id="selectCourse"
          onChange={(e) => {
            setSelected(false);
            setClassInfo({
              enrollment: 0,
              capacity: 0,
              type: "",
              cost: 0,
              classroom: "NA",
              teacher: "NA",
              course_start: "NA",
              course_end: "NA",
            });
            const selected_course = findSelectedCourse(courses, e.target.value);
            if (selected_course !== null) {
              setCourseSelection(selected_course);

              setClassInfo({
                enrollment: selected_course.enrollment,
                capacity: selected_course.size_limit,
                cost: selected_course.cost,
                type: selected_course.course_type,
                classroom: selected_course.classroom,
                teacher: selected_course.teacher,
                course_start: selected_course.course_start_time,
                course_end: selected_course.course_end_time,
              });
              setCost(selected_course.cost);
              setSelected(true);
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
      {selected && (
        <div className="form-control">
          <label>
            <strong>Class Information</strong>
          </label>
          <div className="input-group pb-2">
            <div className="input-group pb-2">
              <span className="input-group-text bg-info">Time</span>
              <span className="input-group-text bg-white">
                {extractCourseTime(classInfo)}
              </span>
              <span className="input-group-text bg-info">Classroom</span>
              <span className="input-group-text bg-white">
                {classInfo.classroom}
              </span>
              <span className="input-group-text bg-info">Teacher</span>
              <span className="input-group-text bg-white">
                {classInfo.teacher}
              </span>
            </div>
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
            </div>
            <div className="row g-3 input-group pb-2">
              <div className="col-auto">
                <TotalCost amount={cost} />
              </div>
              <div className="col-auto">
                <input
                  type="text"
                  className="form-control col-auto"
                  placeholder="Coupon code"
                  aria-label="Coupon"
                  onChange={(e) => {
                    setCouponCode(e.target.value);
                  }}
                />
              </div>
              <div className="col-auto">
                <input
                  type="button"
                  className="btn btn-outline-primary"
                  value={couponApplied ? "Remove" : "Apply"}
                  id="coupon-button"
                  disabled={waitForResponse}
                  onClick={() => {
                    setWaitForResponse(true);
                    if (!couponApplied && couponCode.length > 0) {
                      GetCoupon(
                        user_auth,
                        couponCode,
                        classInfo.cost,
                        (updatedCost) => {
                          setCost(updatedCost);
                          setCouponApplied(true);
                          populateCouponCode(couponCode);
                        }
                      );
                    } else {
                      setCost(classInfo.cost);
                      setCouponApplied(false);
                      populateCouponCode("");
                    }
                    setWaitForResponse(false);
                  }}
                />
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default CourseSelection;
