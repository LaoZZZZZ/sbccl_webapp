import React, { useEffect, useState } from "react";
import AddRegistration from "./AddRegistration.tsx";
import { fetchStudents } from "./FetchStudents.tsx";
import { fetchCourses } from "./FetchCourses.tsx";
import { UserInfo } from "./UserInfo.tsx";
import fetchRegistrations, {
  RegistrationBundle,
} from "../common/FetchRegistrations.tsx";
import EditableRegistration from "./EditableRegistration.tsx";
import TeacherDetailPage from "./TeacherDetailPage.tsx";
import { FetchDropouts } from "../common/FetchDropouts.tsx";
import DropoutDetails from "../common/DropoutDetails.tsx";
import RegistrationDetails from "../common/RegistrationDetails.tsx";

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
  TeacherDetails: 3,
};

interface PageState {
  pageState: number;
}

const Registrations = ({ userInfo }: Props) => {
  const [registrationState, setRegistrationState] = useState<ValueState>({
    fetched: false,
    value: [],
  });

  const [dropoutState, setDropoutState] = useState<ValueState>({
    fetched: false,
    value: [],
  });

  const [paymentsState, setPaymentsState] = useState<ValueState>({
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
  const [selectedTeacher, setSelectedTeacher] = useState({
    class_name: "",
    teachers_info: [],
  });

  useEffect(() => {
    if (!studentState.fetched) {
      fetchStudents(userInfo, (students) => {
        setStudentState(students);
      });
    }
    if (!courseState.fetched) {
      fetchCourses(userInfo.auth, -1, -1, (response) => {
        setCourseState({
          fetched: true,
          value: response.courses,
        });
      });
    }

    if (!registrationState.fetched) {
      fetchRegistrations(userInfo, (registrations) => {
        setRegistrationState(registrations);
      });
    }

    if (!dropoutState.fetched) {
      FetchDropouts(userInfo.auth, (dropoutInfo) => {
        setDropoutState(dropoutInfo);
      });
    }
  }, [
    userInfo,
    studentState,
    courseState,
    registrationState,
    pageState,
    paymentsState,
  ]);

  const table_columns_names = [
    "Student",
    "Course",
    "School Year",
    "Status",
    "Balance",
    "Teacher",
  ];

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
        </div>
      )}
      <hr className="pb-2" />

      {pageState.pageState === PageStateEnum.ListRegistrations && (
        <>
          {registrationState.fetched && (
            <div>
              <RegistrationDetails
                registrations={registrationState.value}
                showTeacherInfo={(teacher) => {
                  setSelectedTeacher(teacher);
                  setPageState({
                    ...pageState,
                    pageState: PageStateEnum.TeacherDetails,
                  });
                }}
                editRegistration={(r: RegistrationBundle) => {
                  setSelectedRegistration(r);
                  setPageState({
                    ...pageState,
                    pageState: PageStateEnum.EditRegistration,
                  });
                }}
              />
              <hr className="pb-2" />
            </div>
          )}
          <DropoutDetails dropouts={dropoutState.value} />
        </>
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
      {pageState.pageState === PageStateEnum.TeacherDetails && (
        <div>
          <TeacherDetailPage
            class_name={selectedTeacher.class_name}
            teachers_info={selectedTeacher.teachers_info}
            exitCallBack={() => {
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
        </div>
      )}
    </>
  );
};

export default Registrations;
