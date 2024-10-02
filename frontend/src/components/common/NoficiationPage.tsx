import React, { useEffect, useState } from "react";
import { AccountInfo } from "../user/UserInfo";
import TextInput from "./TextInput.tsx";
import validator from "validator";
import {
  sendNotification,
  Notification,
  BroadCastEvent,
} from "./SendNotification.tsx";
import CourseDropList from "./CourseDropList.tsx";
import {
  fetchCourses,
  CourseList,
  ClassInformation,
} from "../user/FetchCourses.tsx";
import Alert from "./Alert.tsx";

interface Props {
  userInfo: AccountInfo;
}

const SendStatus = {
  UNKNOWN: -1,
  SUCCESS: 0,
  FAILED: 1,
};

// Add broadcast group for qualified users
const addBroadcastGroups = (userInfo: AccountInfo) => {
  if (userInfo.user.member_type !== "Board Member") {
    return [];
  }
  return [
    {
      name: "All Parents",
    } as ClassInformation,
    // TODO(luke): Bring these use cases back once the backend supports it.
    {
      name: "All Teachers",
    } as ClassInformation,
    {
      name: "All Teaching Assistants",
    } as ClassInformation,
    {
      name: "All Language Teachers",
    } as ClassInformation,
    {
      name: "All Enrichment Teachers",
    } as ClassInformation,
  ];
};

const getBroadcastEvent = (event) => {
  if (event === "All Parents") {
    return BroadCastEvent.AllParent;
  }
  if (event === "All Teachers") {
    return BroadCastEvent.AllTeacher;
  }
  if (event === "All Teaching Assistants") {
    return BroadCastEvent.AllTeachingAssistant;
  }
  if (event === "All Language Teachers") {
    return BroadCastEvent.AllLanguageTeacher;
  }
  if (event === "All Enrichment Teachers") {
    return BroadCastEvent.AllEnrichmentTeacher;
  }
  return BroadCastEvent.None;
};

export function NoficiationPage({ userInfo }: Props) {
  const [message, setMessage] = useState<Notification>({
    broadcast: BroadCastEvent.None,
    recipient: -1,
    subject: "",
    body: "",
  });
  const [courseState, setCourseState] = useState<CourseList>({
    fetched: false,
    courses: [],
  });

  const [selectedCourse, setSelectedCourse] = useState({
    selected: false,
    course: {},
  });

  const [sendStatus, setSendStatus] = useState({
    status: SendStatus.UNKNOWN,
    errMsg: "",
  });

  useEffect(() => {
    if (!courseState.fetched) {
      fetchCourses(userInfo.auth, -1, -1, (response: CourseList) => {
        setCourseState({
          fetched: response.fetched,
          courses: addBroadcastGroups(userInfo).concat(response.courses),
        });
      });
    }
  }, [courseState, selectedCourse]);

  return (
    <div className="col w-75 mx-auto align-middle">
      <form className="form-label form-control">
        <CourseDropList
          courses={courseState.fetched ? courseState.courses : []}
          retrieveCourseCallback={(selected) => {
            if (selected == null) {
              setSelectedCourse({
                selected: false,
                course: {},
              });
            } else {
              setSelectedCourse({
                selected: true,
                course: selected,
              });
              if (selected.id == null) {
                setMessage({
                  ...message,
                  broadcast: getBroadcastEvent(selected.name),
                });
              } else {
                setMessage({
                  ...message,
                  broadcast: BroadCastEvent.None,
                  recipient: selected.id,
                });
              }
            }
          }}
        />
        <TextInput
          labelText="Subject"
          inputType={"text"}
          requiredInput={true}
          retrieveInput={(value) => {
            setMessage({
              ...message,
              subject: value,
            });
          }}
          validationFunc={(value) => {
            return !validator.isEmpty(value);
          }}
        />
        <div className="card-body">
          <label htmlFor="textInput">
            <strong>*Body</strong>
          </label>
          {/* Text input box with scrollbar */}
          <textarea
            className="form-control"
            rows={5}
            style={{ resize: "vertical" }} // Allows vertical resizing only
            onChange={(e) =>
              setMessage({
                ...message,
                body: e.target.value,
              })
            }
          ></textarea>
        </div>
        <div className="btn-group pt-2">
          <input
            className="btn btn-primary active mr-2"
            type="button"
            value="Send"
            disabled={
              !selectedCourse.selected ||
              message.subject.length === 0 ||
              message.body.length === 0
            }
            onClick={() => {
              sendNotification(
                userInfo.auth,
                message,
                () => {
                  setSendStatus({
                    status: SendStatus.SUCCESS,
                    errMsg: "",
                  });
                },
                (error) => {
                  setSendStatus({
                    status: SendStatus.FAILED,
                    errMsg: "Failed to send notification: " + error,
                  });
                }
              );
            }}
          />
        </div>
      </form>
      {sendStatus["status"] === SendStatus.FAILED && (
        <div>
          <Alert
            success={false}
            message={sendStatus.errMsg}
            parentCallback={() => {
              setSendStatus({
                ...sendStatus,
                status: SendStatus.UNKNOWN,
              });
            }}
          />
        </div>
      )}
      {sendStatus["status"] === SendStatus.SUCCESS && (
        <div>
          <Alert
            success={true}
            message={"Notification has been sent out successfully!"}
            parentCallback={() => {
              setSendStatus({
                ...sendStatus,
                status: SendStatus.UNKNOWN,
              });
            }}
          />
        </div>
      )}
    </div>
  );
}
