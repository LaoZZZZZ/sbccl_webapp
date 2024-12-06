import React from "react";
import { useState } from "react";
import TotalCost from "./TotalCost.tsx";
import { GetCoupon, CouponResponse, Coupon } from "./GetCoupon.tsx";
import Alert from "./Alert.tsx";
import {
  ClassInformation,
  getShownName,
  findSelectedCourse,
} from "../user/FetchCourses.tsx";
import { CourseInfo } from "./CourseInfo.tsx";

// Checks if a full course should show on the dropdown.
const shouldShowFullCcourse = (course: ClassInformation) => {
  if (process.env.REACT_APP_COURSE_EXCHANGE_CUTOFF_DATE == null) {
    return true;
  }
  return (
    new Date(process.env.REACT_APP_COURSE_EXCHANGE_CUTOFF_DATE) >= new Date() ||
    course.enrollment < course.size_limit
  );
};

interface Props {
  user_auth: {};
  courses: ClassInformation[];
  defaultCourseSelection: "";
  textbookOrdered: boolean;
  existingCoupon: Coupon;
  setCourseSelection: (course: ClassInformation) => {};
  populateCouponCode: (code: string) => {};
  setOrderBook: (orderBook: boolean) => {};
  disableCourseDropDown?: boolean;
}

const CourseSelection = ({
  user_auth,
  courses,
  defaultCourseSelection,
  textbookOrdered,
  existingCoupon,
  setCourseSelection,
  populateCouponCode,
  setOrderBook,
  disableCourseDropDown,
}: Props) => {
  const [wantTextBook, setWantTextBook] = useState(textbookOrdered);
  const selectedCourse = findSelectedCourse(courses, defaultCourseSelection);
  const [selected, setSelected] = useState(selectedCourse !== null);

  // Hold the information of selected class. Initial values are set to null/0 if there is solection
  const [classInfo, setClassInfo] = useState<ClassInformation>({
    enrollment: selectedCourse !== null ? selectedCourse.enrollment : 0,
    size_limit: selectedCourse !== null ? selectedCourse.size_limit : 0,
    teacher: selectedCourse != null ? selectedCourse.teacher : "NA",
    cost: selectedCourse !== null ? selectedCourse.cost : 0,
    course_type: selectedCourse !== null ? selectedCourse.course_type : "",
    classroom: selectedCourse !== null ? selectedCourse.classroom : "NA",
    course_start_time:
      selectedCourse !== null ? selectedCourse.course_start_time : "NA",
    course_end_time:
      selectedCourse !== null ? selectedCourse.course_end_time : "NA",
    book_cost: selectedCourse !== null ? selectedCourse.book_cost : 0,
    course_description:
      selectedCourse !== null ? selectedCourse.course_description : "",
    name: selectedCourse !== null ? selectedCourse.name : "",
    id: selectedCourse !== null ? selectedCourse.id : 0,
  });
  const [waitForResponse, setWaitForResponse] = useState(false);

  const [coupon, setCoupon] = useState<CouponResponse>({
    errMsg: "",
    couponDetails: existingCoupon,
  });

  const [couponApplied, setCouponApplied] = useState(existingCoupon !== null);
  const calculateOriginalAmount = (registrationCost) => {
    return registrationCost + (wantTextBook ? classInfo.book_cost : 0);
  };

  const calculateUpdatedAmount = (registrationCost) => {
    const totalCost = calculateOriginalAmount(registrationCost);

    if (coupon.couponDetails !== null) {
      if (coupon.couponDetails.type === "A") {
        return Math.max(0, totalCost - coupon.couponDetails.dollar_amount);
      } else if (coupon.couponDetails.type === "P") {
        return (totalCost * (100 - coupon.couponDetails.percentage)) / 100.0;
      }
    }
    return totalCost;
  };
  return (
    <>
      <div className="form-group pb-2">
        <label>
          <strong>Select class</strong>
        </label>
        <select
          className="form-control"
          id="selectCourse"
          disabled={disableCourseDropDown}
          onChange={(e) => {
            setSelected(false);
            setClassInfo({
              enrollment: 0,
              size_limit: 0,
              course_type: "",
              cost: 0,
              classroom: "NA",
              teacher: "Unassigned",
              course_start_time: "NA",
              course_end_time: "NA",
              book_cost: 0,
              course_description: "",
              name: "",
              id: 0,
            });
            const selected_course = findSelectedCourse(courses, e.target.value);
            if (selected_course !== null) {
              setCourseSelection(selected_course);
              setClassInfo({
                enrollment: selected_course.enrollment,
                size_limit: selected_course.size_limit,
                cost: selected_course.cost,
                course_type: selected_course.course_type,
                classroom: selected_course.classroom,
                teacher:
                  selected_course.teacher === ""
                    ? "Unassigned"
                    : selected_course.teacher,
                course_start_time: selected_course.course_start_time,
                course_end_time: selected_course.course_end_time,
                book_cost:
                  selected_course.book_cost !== ""
                    ? selected_course.book_cost
                    : 0,
                course_description: selected_course.course_description,
                name: selected_course.name,
                id: selected_course.id,
              });
              setSelected(true);
            }
          }}
        >
          <option>{defaultCourseSelection}</option>
          {courses
            .filter((course) => {
              return (
                course.name !== defaultCourseSelection &&
                shouldShowFullCcourse(course)
              );
            })
            .map((course) => {
              return <option>{getShownName(course)}</option>;
            })}
        </select>
      </div>
      {selected && (
        <div className="form-control">
          <CourseInfo classInfo={classInfo} />
          <div className="form-check pb-2">
            <input
              className="form-check-input"
              type="checkbox"
              value=""
              id="orderBook"
              onChange={(e) => {
                if (e.target.checked) {
                  setWantTextBook(true);
                  setOrderBook(true);
                } else {
                  setWantTextBook(false);
                  setOrderBook(false);
                }
              }}
              disabled={classInfo.course_type === "E"}
              checked={wantTextBook}
            />
            <label className="form-check-label">
              Order textbook (${classInfo.book_cost})
            </label>
          </div>
          <div className="row g-3 input-group">
            <div className="col-auto">
              <TotalCost
                original_amount={calculateOriginalAmount(classInfo.cost)}
                updated_amount={calculateUpdatedAmount(classInfo.cost)}
              />
            </div>
            <div className="col-auto">
              <input
                type="text"
                className="form-control col-auto"
                placeholder="Enter Coupon Code"
                value={
                  coupon.couponDetails === null ? "" : coupon.couponDetails.code
                }
                aria-label="Coupon"
                disabled={
                  existingCoupon !== null ||
                  calculateUpdatedAmount(classInfo.cost) === 0
                }
                onClick={(e) => {
                  if (e.target.value === "Enter Coupon Code") {
                    e.target.value = "";
                  }
                }}
                onmouseleave={(e) => {
                  if (e.target.value == "") {
                    e.target.value = "Enter Coupon Code";
                  }
                }}
                onChange={(e) => {
                  setCoupon({
                    errMsg: "",
                    couponDetails: {
                      code: e.target.value,
                    },
                  });
                }}
              />
            </div>
            <div className="col-auto">
              <input
                type="button"
                className="btn btn-outline-primary"
                value={couponApplied ? "Remove" : "Apply"}
                id="coupon-button"
                disabled={
                  waitForResponse ||
                  calculateUpdatedAmount(classInfo.cost) === 0 ||
                  existingCoupon !== null
                }
                onClick={() => {
                  setWaitForResponse(true);
                  if (!couponApplied && coupon.couponDetails !== null) {
                    GetCoupon(
                      user_auth,
                      coupon.couponDetails.code,
                      (coupon) => {
                        setCoupon(coupon);
                        calculateOriginalAmount(classInfo.cost);
                        if (coupon.couponDetails !== null) {
                          setCouponApplied(true);
                          populateCouponCode(coupon.couponDetails.code);
                        }
                      }
                    );
                  } else {
                    // Remove code
                    setCoupon({
                      errMsg: "",
                      couponDetails: null,
                    });
                    setCouponApplied(false);
                    populateCouponCode("");
                  }
                  setWaitForResponse(false);
                }}
              />
            </div>
            {coupon.errMsg.length !== 0 && (
              <div>
                <Alert
                  message={coupon.errMsg}
                  parentCallback={function (): void {
                    setCoupon({
                      errMsg: "",
                      couponDetails: null,
                    });
                  }}
                ></Alert>
              </div>
            )}
          </div>
        </div>
      )}
    </>
  );
};

export default CourseSelection;
