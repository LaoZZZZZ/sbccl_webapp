import React, { useEffect, useState } from "react";
import AddRegistration from "./AddRegistration.tsx";
import fetchStudents from "./FetchStudents.tsx";
import fetchCourses from "./FetchCourses.tsx";
import UserInfo from "./UserInfo.tsx";
import fetchRegistrations from "./FetchRegistrations.tsx";
import EditableRegistration from "./EditableRegistration.tsx";

interface Props {
  userInfo: UserInfo;
}

interface ValueState {
  fetched: boolean;
  value: [];
}

const PageStateEnum = {
  ListRegistrations: 0,
  AddRegistration: 1,
  EditRegistration: 2,
};

interface PageState {
  pageState: number;
}

const renderRegistration = (registration) => {
  return (
    registration["student"]["last_name"] +
    " " +
    registration["student"]["first_name"] +
    " - " +
    registration["course"]["name"]
  );
};

const Registrations = ({ userInfo }: Props) => {
  const [registrationState, setRegistrationState] = useState<ValueState>({
    fetched: false,
    value: [],
  });

  const [studentState, setStudentState] = useState<ValueState>({
    fetched: false,
    value: [],
  });

  const [courseState, setCourseState] = useState<ValueState>({
    fetched: false,
    value: [],
  });

  const [pageState, setPageState] = useState<PageState>({
    pageState: PageStateEnum.ListRegistrations,
  });

  const [selectedRegistration, setSelectedRegistration] = useState({});

  useEffect(() => {
    if (!studentState.fetched) {
      fetchStudents(userInfo, (students) => {
        setStudentState(students);
      });
    }
    if (!courseState.fetched) {
      fetchCourses(userInfo, (courses) => {
        setCourseState(courses);
      });
    }

    if (!registrationState.fetched) {
      fetchRegistrations(userInfo, (registrations) => {
        setRegistrationState(registrations);
      });
    }
  }, [userInfo, studentState, courseState, registrationState, pageState]);

  return (
    <>
      {pageState.pageState === PageStateEnum.ListRegistrations && (
        <div>
          <button
            type="button"
            className="btn btn-primary"
            onClick={() => {
              setPageState({
                ...pageState,
                pageState: PageStateEnum.AddRegistration,
              });
            }}
          >
            Register class
          </button>
          <hr className="pb-2" />
        </div>
      )}
      {pageState.pageState === PageStateEnum.ListRegistrations && (
        <div>
          <ul className="list-group pb-2">
            {registrationState.fetched && (
              <caption>List of active registrations</caption>
            )}
            {registrationState.value.map((r) => {
              return (
                <li className="pb-2">
                  <button
                    className="btn btn-secondary bg-info"
                    onClick={(e) => {
                      setSelectedRegistration(r);
                      setPageState({
                        ...pageState,
                        pageState: PageStateEnum.EditRegistration,
                      });
                    }}
                  >
                    {renderRegistration(r)}
                  </button>
                </li>
              );
            })}
          </ul>
        </div>
      )}
      {pageState.pageState === PageStateEnum.AddRegistration && (
        <AddRegistration
          userAuth={userInfo.auth}
          students={studentState.value}
          courses={courseState.value}
          updateRegistrationList={() => {
            setRegistrationState({ fetched: false, value: [] });
            setCourseState({ fetched: false, value: [] });
            return setPageState({
              ...pageState,
              pageState: PageStateEnum.ListRegistrations,
            });
          }}
          cancelCallback={() => {
            setRegistrationState({
              fetched: true,
              value: registrationState.value,
            });
            return setPageState({
              ...pageState,
              pageState: PageStateEnum.ListRegistrations,
            });
          }}
        />
      )}
      <hr className="pb-2" />
      {pageState.pageState === PageStateEnum.EditRegistration && (
        <EditableRegistration
          userAuth={userInfo.auth}
          selectedRegistration={selectedRegistration}
          courses={courseState.value}
          updateRegistrationList={() => {
            setRegistrationState({ fetched: false, value: [] });
            setCourseState({ fetched: false, value: [] });
            return setPageState({
              ...pageState,
              pageState: PageStateEnum.ListRegistrations,
            });
          }}
          cancelCallback={() => {
            setRegistrationState({
              fetched: true,
              value: registrationState.value,
            });
            return setPageState({
              ...pageState,
              pageState: PageStateEnum.ListRegistrations,
            });
          }}
        />
      )}
    </>
  );
};

export default Registrations;
