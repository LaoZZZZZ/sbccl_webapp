import axios from "axios";
import ModelWindow from "../common/ModelWindow.tsx";
import React, { useState } from "react";
import Alert from "../common/Alert.tsx";

interface Props {
  student: {};
  courseName: string;
  registration: {};
  userAuth: {};
  callBackUponSuccessRemoval: {};
  callBackUponExit: () => {};
}

const RemoveStatus = {
  UNSPECIFIED: 0,
  SUCCESS: 1,
  FAILED: 2,
};

const DeleteRegistrationRequest = async (registration, authInfo, callBack) => {
  await axios
    .put(
      "http://localhost:8000/rest_api/members/" +
        registration.id +
        "/unregister-course/",
      {},
      {
        auth: authInfo,
      }
    )
    .then(function (response) {
      if (response.status === 202) {
        callBack({
          status: RemoveStatus.SUCCESS,
          msg: "The registration has been successfully removed!",
        });
      }
    })
    .catch((e) => {
      callBack({
        status: RemoveStatus.FAILED,
        msg: JSON.stringify(e.response.data),
      });
    });
};

const RemoveRegistration = ({
  student,
  courseName,
  registration,
  userAuth,
  callBackUponSuccessRemoval,
  callBackUponExit,
}: Props) => {
  const title: string = "Class drop out";
  const body: string =
    "Are you sure to remove " +
    student.last_name +
    " " +
    student.first_name +
    " from class " +
    courseName;
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
            return DeleteRegistrationRequest(
              registration,
              userAuth,
              setRemoveStatus
            );
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

export default RemoveRegistration;
