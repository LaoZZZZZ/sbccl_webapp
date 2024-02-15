import React, { useEffect, useState } from "react";
import AddRegistration from "./AddRegistration.tsx";
import fetchStudents from "./FetchStudents.tsx";
import fetchCourses from "./FetchCourses.tsx";
import UserInfo from "./UserInfo.tsx";
import fetchRegistrations from "./FetchRegistrations.tsx";

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
};

interface PageState {
  pageState: number;
}

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
        <button
          type="button"
          className="btn btn-info"
          onClick={() => {
            setPageState({
              ...pageState,
              pageState: PageStateEnum.AddRegistration,
            });
          }}
        >
          Register class
        </button>
      )}
      <hr className="pb-2" />
      {pageState.pageState === PageStateEnum.ListRegistrations && (
        <ul className="list-group pb-2">
          <caption>List of active registrations</caption>
          {registrationState.value.map((r) => {
            return (
              <li className="pb-2">
                <button>{r["registration_code"]}</button>
              </li>
            );
          })}
        </ul>
      )}
      {pageState.pageState === PageStateEnum.AddRegistration && (
        <AddRegistration
          userAuth={userInfo.auth}
          students={studentState.value}
          courses={courseState.value}
          updateRegistrationList={() => {
            setRegistrationState({ fetched: false, value: [] });
            return setPageState({
              ...pageState,
              pageState: PageStateEnum.ListRegistrations,
            });
          }}
          cancelCallback={() => {
            setRegistrationState({
              fetched: false,
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
      <p>Past Registrations</p>
    </>
  );
};

export default Registrations;
