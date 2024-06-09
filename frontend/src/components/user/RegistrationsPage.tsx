import React, { useEffect, useState } from "react";
import AddRegistration from "./AddRegistration.tsx";
import fetchStudents from "./FetchStudents.tsx";
import fetchCourses from "./FetchCourses.tsx";
import UserInfo from "./UserInfo.tsx";
import fetchRegistrations from "../common/FetchRegistrations.tsx";
import EditableRegistration from "./EditableRegistration.tsx";
import TeacherDetailPage from "./TeacherDetailPage.tsx";
import {
  FetchPayments,
  Payment,
  PaymentsResponse,
} from "../common/FetchPayments.tsx";

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

const renderRegistration = (registration) => {
  return (
    registration["student"]["last_name"] +
    " " +
    registration["student"]["first_name"]
  );
};

const calculateBalance = (registration) => {
  if (registration["payments"]) {
    return (
      "$" +
      (
        registration["payments"].original_amount -
        registration["payments"].amount_in_dollar
      ).toString()
    );
  }
  return "$0";
};

const Registrations = ({ userInfo }: Props) => {
  const [registrationState, setRegistrationState] = useState<ValueState>({
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
      fetchCourses(userInfo, (courses) => {
        setCourseState(courses);
      });
    }

    if (!registrationState.fetched) {
      fetchRegistrations(userInfo, (registrations) => {
        setRegistrationState(registrations);
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

      {pageState.pageState === PageStateEnum.ListRegistrations &&
        registrationState.fetched && (
          <div className="table-responsive">
            <table className="table table-bordered table-hover table-striped">
              <caption>List of registrations</caption>
              <thead>
                <tr id="column_name">
                  {table_columns_names.map((colmunName) => {
                    return <th scope="col">{colmunName}</th>;
                  })}
                </tr>
              </thead>
              <tbody>
                {registrationState.value.map((r) => (
                  <tr>
                    <td>
                      <button
                        className={"btn btn-outline-secondary"}
                        data-toggle="modal"
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
                    </td>
                    <td>{r["course"]["name"]}</td>
                    <td>
                      {new Date(
                        r["registration"]["school_year_start"]
                      ).getFullYear() +
                        " - " +
                        new Date(
                          r["registration"]["school_year_end"]
                        ).getFullYear()}
                    </td>
                    <td>
                      {r["registration"]["on_waiting_list"]
                        ? "On Waiting List"
                        : "Enrolled"}
                    </td>
                    <td>{calculateBalance(r)}</td>
                    <td>
                      <button
                        className={"btn btn-outline-secondary"}
                        data-toggle="modal"
                        onClick={(e) => {
                          setSelectedTeacher({
                            class_name: r["course"]["name"],
                            teachers_info: r["teacher"],
                          });
                          setPageState({
                            ...pageState,
                            pageState: PageStateEnum.TeacherDetails,
                          });
                        }}
                      >
                        Teacher information
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <hr className="pb-2" />
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
