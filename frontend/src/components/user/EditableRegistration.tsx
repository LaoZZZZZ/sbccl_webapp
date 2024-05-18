import React, { useState } from "react";
import Alert from "../common/Alert.tsx";
import axios from "axios";
import CourseSelection from "../common/CourseSelection.tsx";
import RemoveRegistration from "./RemoveRegistrationPage.tsx";

interface Student {
  first_name: string;
  last_name: string;
  date_of_birth: Date;
  gender: string;
}

interface Props {
  userAuth: {};
  selectedRegistration: {};
  courses: [];
  updateRegistrationList: () => {};
  cancelCallback: () => {};
}

const UpdateStatus = {
  SUCCESS: 0,
  FAILED: 1,
};

const GenerateStudentInfo = (student: Student) => {
  return (
    student.last_name +
    " " +
    student.first_name +
    "(" +
    student.date_of_birth +
    ")"
  );
};

const UpdateRegistrationRequest = async (registration, authInfo, callBack) => {
  await axios
    .put(
      process.env.REACT_APP_BE_URL_PREFIX +
        "/rest_api/members/update-registration/",
      registration,
      {
        auth: authInfo,
      }
    )
    .then(function (response) {
      if (response.status === 202) {
        callBack({
          status: UpdateStatus.SUCCESS,
          msg: "Congratulations. The registration has been successfully updated!",
        });
      }
    })
    .catch((e) => {
      callBack({
        status: UpdateStatus.FAILED,
        msg: JSON.stringify(e.response.data.detail),
      });
    });
};

const DeleteRegistration = async (registration, authInfo, callBack) => {
  const registration_id = registration["id"];
  await axios
    .put(
      "http://" +
        process.env.BE_URL_PREFIX +
        "/rest_api/members/" +
        registration_id +
        "/unregister-course/",
      {},
      {
        auth: authInfo,
      }
    )
    .then(function (response) {
      if (response.status === 202) {
        callBack({
          status: UpdateStatus.SUCCESS,
          msg: "Congratulations. The registration has been successfully updated!",
        });
      }
    })
    .catch((e) => {
      callBack({
        status: UpdateStatus.FAILED,
        msg: JSON.stringify(e.response.data),
      });
    });
};

const EditableRegistration = ({
  userAuth,
  selectedRegistration,
  courses,
  updateRegistrationList,
  cancelCallback,
}: Props) => {
  const [updateStatus, setUpdateStatus] = useState({});
  const student = selectedRegistration["student"];
  const registration = selectedRegistration["registration"];
  const originalCourse = selectedRegistration["course"];

  const coupons =
    selectedRegistration["coupons"] === null ||
    selectedRegistration["coupons"].length === 0
      ? null
      : selectedRegistration["coupons"][0];
  const [buttonMsg, setButtonMsg] = useState("Update");
  const [needsUpdate, setNeedsUpdate] = useState<boolean>(false);
  const [removeRegistration, setRemoveRegistration] = useState(false);
  const [waitForResponse, setWaitForResponse] = useState(false);

  return (
    <div className="col w-75 mx-auto align-middle">
      {!removeRegistration && (
        <form className="form-label form-control">
          <div className="form-group pb-2 mb-2">
            <label className="sr-only" htmlFor="student">
              <strong>Student</strong>
            </label>
            <input
              className="form-control"
              type="text"
              id="student"
              readOnly
              value={student.last_name + " " + student.first_name}
              disabled
            />
          </div>
          <div className="form-group pb-2 mb-2">
            <label className="sr-only" htmlFor="school-year">
              <strong>School Year</strong>
            </label>
            <input
              className="form-control"
              type="text"
              id="school-year"
              readOnly
              value={
                new Date(registration.school_year_start).getFullYear() +
                "-" +
                new Date(registration.school_year_end).getFullYear()
              }
              disabled
            />
          </div>
          <div className="form-group pb-2 mb-2">
            <CourseSelection
              user_auth={userAuth}
              courses={courses.filter((course) => {
                return course.course_type === originalCourse.course_type;
              })}
              defaultCourseSelection={originalCourse.name}
              setCourseSelection={(course) => {
                const update = originalCourse.id !== course.id;
                setNeedsUpdate(update);
                setButtonMsg(
                  course.enrollment >= course.size_limit && needsUpdate
                    ? "Add to waiting list"
                    : "Update"
                );
                return (registration.course = course.id);
              }}
              populateCouponCode={(code: string) => {
                if (code.length > 0) {
                  setNeedsUpdate(
                    registration.coupons === null ||
                      registration.coupons.length === 0
                  );
                  registration.coupons = [code];
                } else {
                  registration.coupons = [];
                  setNeedsUpdate(false);
                }
              }}
              setOrderBook={(orderBook: boolean) => {
                setNeedsUpdate(registration.textbook_ordered !== orderBook);

                registration.textbook_ordered = orderBook;
              }}
              textbookOrdered={registration["textbook_ordered"]}
              existingCoupon={coupons}
            />
          </div>
          <div className="form-group pb-2 mb-2">
            <label className="sr-only" htmlFor="registration-code">
              <strong>Registration Code</strong>
            </label>
            <input
              className="form-control"
              type="text"
              id="registration-date"
              readOnly
              value={registration.registration_code}
              disabled
            />
          </div>

          <div className="form-group pb-2 mb-2">
            <label className="sr-only" htmlFor="registration-date">
              <strong>Registration Date</strong>
            </label>
            <input
              className="form-control"
              type="text"
              id="registration-date"
              readOnly
              value={registration.registration_date}
              disabled
            />
          </div>
          <div className="btn-group pt-2">
            <input
              className="btn btn-primary active mr-3"
              type="button"
              disabled={!needsUpdate || waitForResponse}
              value={buttonMsg}
              onClick={() => {
                console.log(registration);
                setWaitForResponse(true);
                UpdateRegistrationRequest(registration, userAuth, (result) => {
                  setUpdateStatus(result);
                  if (result.status === UpdateStatus.SUCCESS) {
                    updateRegistrationList();
                  }
                  setWaitForResponse(false);
                });
              }}
            />
            <input
              className="btn btn-secondary mr-3"
              type="button"
              value="Cancel"
              onClick={() => {
                cancelCallback();
              }}
              disabled={waitForResponse}
            />
            <input
              className="btn btn-warning mr-3"
              type="button"
              value="Delete"
              onClick={() => {
                setRemoveRegistration(true);
              }}
              disabled={waitForResponse}
            />
          </div>
        </form>
      )}
      {updateStatus["status"] === UpdateStatus.FAILED && (
        <div>
          <Alert
            success={false}
            message={updateStatus["msg"]}
            parentCallback={() => {
              setUpdateStatus({});
            }}
          />
        </div>
      )}
      {removeRegistration && (
        <RemoveRegistration
          student={student}
          courseName={originalCourse.name}
          registration={registration}
          userAuth={userAuth}
          callBackUponSuccessRemoval={() => {
            updateRegistrationList();
          }}
          callBackUponExit={() => {
            setRemoveRegistration(false);
          }}
        />
      )}
    </div>
  );
};

export default EditableRegistration;
