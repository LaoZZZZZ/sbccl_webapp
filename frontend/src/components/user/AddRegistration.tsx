import React, { useState } from "react";
import Alert from "../common/Alert.tsx";
import axios from "axios";
import CourseSelection from "../common/CourseSelection.tsx";

interface Props {
  userAuth: {};
  students: [];
  courses: [];
  updateRegistrationList: () => {};
  cancelCallback: () => {};
}

interface Student {
  first_name: string;
  last_name: string;
  date_of_birth: Date;
  gender: string;
}

// Json format for the data model of backend API call.
interface Registration {
  course_id: string;
  student: Student;
  pod: string;
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
      process.env.REACT_APP_BE_URL_PREFIX +
        "/rest_api/members/register-course/",
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
      callBack({
        status: AddStatus.FAILED,
        msg: JSON.stringify(e.response.data),
      });
    });
};

const AddRegistration = ({
  userAuth,
  students,
  courses,
  updateRegistrationList,
  cancelCallback,
}: Props) => {
  const [addStatus, setAddStatus] = useState({});
  const [buttonMsg, setButtonMsg] = useState("Register");

  const [registration] = useState<Registration>({
    course_id: "",
    student: {
      last_name: "",
      first_name: "",
      gender: "",
      date_of_birth: new Date("1997-01-01"),
    },
    pod: "",
  });

  return (
    <div className="col w-75 mx-auto align-middle">
      <form className="form-label form-control">
        <div className="form-group pb-2">
          <label>Select student</label>
          <select
            className="form-control"
            id="studentSelect"
            onChange={(e) => {
              const selected_student = students.filter(
                (student: Student) =>
                  e.target.value.includes(student.date_of_birth) &&
                  e.target.value.includes(student.first_name)
              );
              if (selected_student.length === 1)
                registration.student = selected_student[0];
            }}
          >
            <option>Not Selected</option>
            {students.map((student) => {
              return <option>{GenerateStudentInfo(student)}</option>;
            })}
          </select>
        </div>
        <CourseSelection
          courses={courses}
          defaultCourseSelection={"Not Selected"}
          defaultPoDSelection={"Not Selected"}
          setCourseSelection={(course) => {
            setButtonMsg(
              course.enrollment < course.size_limit
                ? "Register"
                : "Add to waiting list"
            );
            registration.course_id = course.id;
          }}
          setPoDSelection={(pod) => {
            return (registration.pod = pod);
          }}
        />
        <div className="btn-group pt-2">
          <input
            className="btn btn-primary active mr-2"
            type="button"
            value={buttonMsg}
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
      {addStatus["status"] === AddStatus.FAILED && (
        <div>
          <Alert
            success={false}
            message={addStatus["msg"]}
            parentCallback={() => {
              setAddStatus({});
            }}
          />
        </div>
      )}
    </div>
  );
};

export default AddRegistration;
