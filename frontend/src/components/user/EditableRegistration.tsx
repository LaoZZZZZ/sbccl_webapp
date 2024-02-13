import React, { useState } from "react";
import Alert from "../common/Alert.tsx";
import axios from "axios";

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
      "http://localhost:8000/rest_api/members/register-course/",
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

const AddRegistration = ({
  userAuth,
  students,
  courses,
  updateRegistrationList,
  cancelCallback,
}: Props) => {
  const [addStatus, setAddStatus] = useState({});
  const [registration] = useState<Registration>({
    course_id: "",
    student: {
      last_name: "",
      first_name: "",
      gender: "",
      date_of_birth: new Date("1997-01-01"),
    },
  });

  return (
    <div className="col w-75 mx-auto align-middle">
      <form className="form-label form-control">
        <input
          className="form-control"
          type="text"
          placeholder="Disabled input"
          aria-label="Disabled input example"
          disabled
        />

        <div className="form-group">
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
        <div className="form-group">
          <label>Select class</label>
          <select
            className="form-control"
            id="selectCourse"
            onChange={(e) => {
              const selected_course = courses.filter(
                (course) => e.target.value === course.name
              );
              if (selected_course.length === 1)
                registration.course_id = selected_course[0].id;
            }}
          >
            <option>Not Selected</option>

            {courses.map((course) => {
              return <option>{course.name}</option>;
            })}
          </select>
        </div>
        <div className="btn-group pt-2">
          <input
            className="btn btn-primary active mr-2"
            type="button"
            value="Add"
            onClick={() => {
              console.log(registration);
              AddRegistrationRequest(registration, userAuth, (result) => {
                setAddStatus(result);
                if (result.status == AddStatus.SUCCESS) {
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
        <Alert
          success={false}
          message={addStatus["msg"]}
          parentCallback={() => {
            setAddStatus({});
          }}
        />
      )}
    </div>
  );
};

export default AddRegistration;
