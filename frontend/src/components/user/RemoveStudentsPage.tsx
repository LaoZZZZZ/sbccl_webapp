import axios from "axios";
import ModelWindow from "../common/ModelWindow.tsx";
import React, { useState } from "react";
import Alert from "../common/Alert.tsx";

interface Props {
  studentInfo: {};
  userAuth: {};
  callBackUponSuccessRemoval: {};
  callBackUponExit: () => {};
}

const RemoveStatus = {
  UNSPECIFIED: 1,
  SUCCESS: 2,
  FAILED: 3,
};

const RemoveStudentRequest = async (student, authInfo, callBack) => {
  await axios
    .put(
<<<<<<< HEAD
      process.env.REACT_APP_BE_URL_PREFIX + "/rest_api/members/remove-student/",
=======
      "http://" +
        process.env.REACT_APP_BE_URL_PREFIX +
        "/rest_api/members/remove-student/",
>>>>>>> a0582317 (Parameterize backend hostname.)
      student,
      {
        auth: authInfo,
      }
    )
    .then(function (response) {
      if (response.status === 202) {
        callBack({
          status: RemoveStatus.SUCCESS,
          msg: "The selected student was removed from your account!",
        });
      }
    })
    .catch((e) => {
      console.log(e.response.data);
      callBack({
        status: RemoveStatus.FAILED,
        msg: JSON.stringify(e.response.data),
      });
    });
};

const RemoveStudents = ({
  studentInfo,
  userAuth,
  callBackUponSuccessRemoval,
  callBackUponExit,
}: Props) => {
  const title: string = "Remove students";
  const body: string =
    "Are you sure to remove " +
    studentInfo.last_name +
    " " +
    studentInfo.first_name +
    " from your account?";
  const [removeStatus, setRemoveStatus] = useState({
    status: RemoveStatus.UNSPECIFIED,
    msg: "",
  });
  return (
    <>
      {removeStatus.status === RemoveStatus.UNSPECIFIED && (
        <ModelWindow
          title={title}
          bodyMsg={body}
          callBackUponConfirm={() => {
            return RemoveStudentRequest(studentInfo, userAuth, setRemoveStatus);
          }}
          dismissCallback={callBackUponExit}
        />
      )}
      {removeStatus.status !== RemoveStatus.UNSPECIFIED && (
        <Alert
          success={removeStatus.status === RemoveStatus.SUCCESS}
          message={removeStatus.msg}
          parentCallback={callBackUponSuccessRemoval}
        />
      )}
    </>
  );
};

export default RemoveStudents;
