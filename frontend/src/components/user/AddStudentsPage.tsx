import React, { useState } from "react";
import TextInput from "../common/TextInput.tsx";
import validator from "validator";
import Alert from "../common/Alert.tsx";
import axios from "axios";
import DatePicker from "../common/DatePicker.tsx";

interface Props {
  userAuth: {};
  updateStudentList: () => {};
}

// Json format for the data model of backend API call.
interface Student {
  last_name: string;
  first_name: string;
  middle_name: string;
  date_of_birth: Date;
  gender: string;
  chinese_name: string;
}

const AddStatus = {
  SUCCESS: 0,
  FAILED: 1,
};

const AddStudentRequest = async (student, authInfo, callBack) => {
  await axios
    .put(
<<<<<<< HEAD
<<<<<<< HEAD
      process.env.REACT_APP_BE_URL_PREFIX + "/rest_api/members/add-student/",
=======
      "http://" +
        process.env.REACT_APP_BE_URL_PREFIX +
        "/rest_api/members/add-student/",
>>>>>>> a0582317 (Parameterize backend hostname.)
=======
      process.env.REACT_APP_BE_URL_PREFIX + "/rest_api/members/add-student/",
>>>>>>> 4e711736 (use https in remote deployment.)
      student,
      {
        auth: authInfo,
      }
    )
    .then(function (response) {
      if (response.status == 201) {
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

const AddStudents = ({ userAuth, updateStudentList }: Props) => {
  const [addStatus, setAddStatus] = useState({});
  const [student, setStudent] = useState<Student>({
    first_name: "",
    last_name: "",
    middle_name: "",
    gender: "",
    date_of_birth: new Date("1997-01-01"),
    chinese_name: "",
  });

  return (
    <div className="col w-75 mx-auto align-middle">
      <form className="form-label form-control">
        <TextInput
          labelText="First name"
          inputType={"text"}
          requiredInput={true}
          retrieveInput={(firstName) => {
            student.first_name = firstName;
          }}
          validationFunc={(value) => {
            return validator.isAlpha(value);
          }}
        />
        <TextInput
          labelText="Middle name"
          inputType={"text"}
          requiredInput={false}
          retrieveInput={(middleName) => {
            student.middle_name = middleName;
          }}
          validationFunc={(value) => {
            return true;
          }}
        />
        <TextInput
          labelText="Last name"
          inputType={"text"}
          requiredInput={true}
          retrieveInput={(lastName) => {
            student.last_name = lastName;
          }}
          validationFunc={(value) => {
            return validator.isAlpha(value);
          }}
        />
        <TextInput
          labelText="Chinese name"
          inputType={"text"}
          requiredInput={false}
          retrieveInput={(chineseName) => {
            student.chinese_name = chineseName;
          }}
          validationFunc={(value) => {
            return true;
          }}
        />
        <div className="pb-2">
          <label htmlFor="textInput">
            <strong>*Gender</strong>
          </label>
          <select
            className="form-control "
            id="gender"
            onChange={(e) => {
              if (e.target.value === "Male") {
                student.gender = "M";
              } else if (e.target.value === "Female") {
                student.gender = "F";
              } else {
                // Unknown
                student.gender = "U";
              }
            }}
          >
            <option selected>Not specified </option>
            <option>Male</option>
            <option>Female</option>
          </select>
        </div>
        <DatePicker
          requiredInput={true}
          retrieveInput={(dob) => {
            student.date_of_birth = dob;
          }}
        />
        <div className="btn-group pt-2">
          <input
            className="btn btn-primary active mr-2"
            type="button"
            value="Add"
            onClick={() => {
              if (
                student.first_name === "" ||
                student.last_name === "" ||
                student.date_of_birth === null ||
                student.gender === ""
              ) {
                setAddStatus({
                  status: AddStatus.FAILED,
                  msg: "Invalid student information provided. The student can not be added now!",
                });
              }
              AddStudentRequest(student, userAuth, (result) => {
                setAddStatus(result);
                if (result.status == AddStatus.SUCCESS) {
                  updateStudentList();
                }
              });
            }}
          />
          <input
            className="btn btn-secondary mr-2"
            type="button"
            value="Cancel"
            onClick={() => {
              updateStudentList();
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

export default AddStudents;
