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
  SUCCESS: 0,
  FAILED: 1,
};

const RemoveStudentRequest = async (student, authInfo, callBack) => {
  await axios
    .put("http://localhost:8000/rest_api/members/remove-student/", student, {
      auth: authInfo,
    })
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
    status: RemoveStatus.SUCCESS,
    msg: "",
  });
  return (
    <>
      {removeStatus.status === RemoveStatus.SUCCESS && (
        <ModelWindow
          title={title}
          bodyMsg={body}
          callBackUponConfirm={() => {
            return RemoveStudentRequest(studentInfo, userAuth, setRemoveStatus);
          }}
          dismissCallback={callBackUponExit}
        />
      )}
      {removeStatus.status === RemoveStatus.FAILED && (
        <Alert
          success={false}
          message={removeStatus.msg}
          parentCallback={callBackUponSuccessRemoval}
        />
      )}
    </>
  );
};

export default RemoveStudents;
