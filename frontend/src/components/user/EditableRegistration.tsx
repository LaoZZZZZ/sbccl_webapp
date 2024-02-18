import React, { useState } from "react";
import Alert from "../common/Alert.tsx";
import axios from "axios";
import CourseSelection from "../common/CourseSelection.tsx";

interface Student {
  first_name: string;
  last_name: string;
  date_of_birth: Date;
  gender: string;
}

interface Registration {
  registration_code: string;
  school_year_start: Date;
  school_year_end: Date;
  registration_date: Date;
}

interface Props {
  userAuth: {};
  selectedRegistration: {};
  courses: [];
  updateRegistrationList: () => {};
  cancelCallback: () => {};
}

// Json format for the data model of backend API call.
interface Registration {
  course_id: string;
  student: Student;
}

const AddStatus = {
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

const AddRegistrationRequest = async (registration, authInfo, callBack) => {
  await axios
    .put(
      "http://localhost:8000/rest_api/members/update-registration/",
      registration,
      {
        auth: authInfo,
      }
    )
    .then(function (response) {
      if (response.status === 201) {
        callBack({
          status: AddStatus.SUCCESS,
          msg: "Congratulations. A student was successfully added to your account!",
        });
      }
    })
    .catch((e) => {
      console.log(e.response.data);
      callBack({
        status: AddStatus.FAILED,
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
  console.log(selectedRegistration);
  console.log(userAuth);
  console.log(courses);
  const student = selectedRegistration["student"];
  const registration = selectedRegistration["registration"];
  const originalCourse = selectedRegistration["course"];

  return (
    <div className="col w-75 mx-auto align-middle">
      <form className="form-label form-control">
        <div className="form-group pb-2 mb-2">
          <label className="sr-only" htmlFor="student">
            Student
          </label>
          <input
            className="form-control"
            type="text"
            id="student"
            readOnly
            value={student.last_name + " " + student.first_name}
          />
        </div>
        <CourseSelection
          courses={courses}
          defaultCourseSelection={originalCourse.name}
          defaultPoDSelection={"Not Selected"}
          setCourseSelection={(course) => {
            return (registration.course_id = course.id);
          }}
          setPoDSelection={(pod) => {
            return (registration.pod = pod);
          }}
        />
        <div className="btn-group pt-2">
          <input
            className="btn btn-primary active mr-2"
            type="button"
            value={
              !classInfo.selected || classInfo.enrollment < classInfo.capacity
                ? "Register"
                : "Add to Waiting list"
            }
            onClick={() => {
              AddRegistrationRequest(registration, userAuth, (result) => {
                setAddStatus(result);
                if (result.status === AddStatus.SUCCESS) {
                  updateRegistrationList();
                }
              });
            }}
          />
          <input
            className="btn btn-secondary mr-2"
            type="button"
            value="Cancel"
            onClick={() => {
              cancelCallback();
            }}
          />
        </div>
      </form>
      {/* {addStatus["status"] === AddStatus.FAILED && (
        <Alert
          success={false}
          message={addStatus["msg"]}
          parentCallback={() => {
            setAddStatus({});
          }}
        />
      )} */}
    </div>
  );
};

export default EditableRegistration;
