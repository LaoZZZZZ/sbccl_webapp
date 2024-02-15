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

interface ClassInformation {
  selected: boolean;
  enrollment: number;
  capacity: number;
  teacher: string;
  cost: string;
  type: string;
}

const AddRegistration = ({
  userAuth,
  students,
  courses,
  updateRegistrationList,
  cancelCallback,
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
  const [addStatus, setAddStatus] = useState({});
  const [classInfo, setClassInfo] = useState<ClassInformation>({
    selected: false,
    enrollment: 0,
    capacity: 0,
    teacher: "",
    cost: "",
    type: "",
  });

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
        <div className="form-group">
          <label>Select class</label>
          <select
            className="form-control"
            id="selectCourse"
            onChange={(e) => {
              const selected_course = courses.filter(
                (course) => e.target.value === course.name
              );
              if (selected_course.length === 1) {
                registration.course_id = selected_course[0].id;
                setClassInfo({
                  selected: true,
                  enrollment: selected_course[0].enrollment,
                  capacity: selected_course[0].size_limit,
                  cost: "$" + selected_course[0].cost,
                  type: selected_course[0].course_type,
                  teacher: "***",
                });
              } else {
                setClassInfo({
                  selected: false,
                  enrollment: 0,
                  capacity: 0,
                  cost: 0,
                  teacher: "",
                });
              }
            }}
          >
            <option>Not Selected</option>

            {courses.map((course) => {
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
            <span className="input-group-text bg-white">
              {classInfo.teacher}
            </span>
          </div>
        )}
        {classInfo.selected && classInfo.type == "L" && (
          <div className="form-group pb-2">
            <label>Select Parent On Duty date</label>
            <select
              className="form-control"
              id="podSelect"
              onChange={(e) => {
                registration.pod = e.target.value;
              }}
            >
              <option>Not Selected</option>
              {podDates.map((date) => {
                return <option>{date}</option>;
              })}
            </select>
          </div>
        )}
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
