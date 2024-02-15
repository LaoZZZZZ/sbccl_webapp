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

const PageState = {
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
    pageState: PageState.ListRegistrations,
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
  }, [registrationState, pageState]);

  return (
    <>
      {pageState.pageState === PageState.ListRegistrations && (
        <button
          type="button"
          className="btn btn-info"
          onClick={() => {
            setPageState({
              ...pageState,
              pageState: PageState.AddRegistration,
            });
          }}
        >
          Register class
        </button>
      )}
      <hr className="pb-2" />
      {pageState.pageState === PageState.ListRegistrations && (
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
      {pageState.pageState === PageState.AddRegistration && (
        <AddRegistration
          userAuth={userInfo.auth}
          students={studentState.value}
          courses={courseState.value}
          updateRegistrationList={() => {
            setRegistrationState({ fetched: false, value: [] });
            return setPageState({
              ...pageState,
              pageState: PageState.ListRegistrations,
            });
          }}
          cancelCallback={() => {
            setRegistrationState({
              fetched: false,
              value: registrationState.value,
            });
            return setPageState({
              ...pageState,
              pageState: PageState.ListRegistrations,
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
