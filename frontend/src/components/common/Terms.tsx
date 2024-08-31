import React, { useState } from "react";
import { AccountInfo, Auth } from "../user/UserInfo.tsx";
import signTerms from "./SignTerms.tsx";

interface Props {
  userInfo: AccountInfo;
  callback: () => void;
  failureCallback: () => void;
}

export default function Terms({ userInfo, callback, failureCallback }: Props) {
  const [waitForResponse, setWaitForResponse] = useState(false);
  return (
    <div className="col w-75 mx-auto align-middle">
      <h2 className="text-center mx-auto ">
        Terms and Conditions of the Center for Chinese Learning at Stony Brook
        (CCL)
      </h2>
      <form className="form-label form-control">
        <div data-bs-spy="scroll" className="mx-auto">
          <ol className="list-group list-group-numbered ">
            <li className="list-group-item fs-4">
              Responsiblity
              <ul className="list-group fs-6">
                <li className="list-group-item">
                  Parents/legal guardians are fully responsible for their
                  child(ren)’s safety and belongings in all activities
                  associated with the Center for Chinese Learning at Stony Brook
                  (CCL).
                </li>
                <li className="list-group-item">
                  Parents/legal guardians hereby consent and willfully waive
                  their rights to bring claims or legal actions against the CCL
                  staff members (including but not limited to principals, board
                  members, teachers and on-duty parents of the School) or the
                  School itself in case there is any accident or incident in the
                  school premises or on field trips during school activities.
                </li>
              </ul>
            </li>
            <li className="list-group-item fs-4">
              Refund
              <ul className="list-group fs-6">
                <li className="list-group-item">
                  80% refund within the first 4 weeks of the new school year;
                  50% refund prior to the 16th class, and no refund afterwards.
                </li>
                <li className="list-group-item">
                  A written request for withdrawn is required.
                </li>
                <li className="list-group-item">
                  Special situations will be considered on an individual base: a
                  written request and appropriate proof is required. The refund
                  amount will be prorated.
                </li>
              </ul>
            </li>
            <li className="list-group-item fs-4">
              Switching Classes
              <ul className="list-group fs-6">
                <li className="list-group-item">
                  Students who decide to switch the class should submit a
                  written request by using the appropriate form
                  (http://www.sbcclny.com/forms) with his/her reasons within the
                  first 4 weeks of the academic year. No request will be
                  accepted after the 4th week unless approved by the CCL board.
                </li>
                <li className="list-group-item">
                  A qualifying exam may be required. The student can attend the
                  requested class only after the request is approved by the
                  board.
                </li>
              </ul>
            </li>
            <li className="list-group-item fs-4">
              Class Trials and Cancellations
              <ul className="list-group fs-6">
                <li className="list-group-item">
                  Trial class is limited to one time per child. If the parents
                  decide to register after the trial, then the registration fee
                  should cover the trial class and the rest of the school year;
                  if the parents decide not to register after the trial, the
                  trial class will be free of charge.
                </li>
                <li className="list-group-item">
                  CCL reserves the right to change or cancel any language or
                  enrichment class due to reasons such as insufficient
                  enrollments (minimum class size is 5 students), lack of
                  classrooms etc. without prior notice.
                </li>
              </ul>
            </li>
            <li className="list-group-item fs-4">
              Deciplines
              <ul className="list-group fs-6">
                <li className="list-group-item">
                  All students must follow the safety guidelines of the school
                  and the instructions from the teachers. Please see details in
                  “School Regulations on School Orders & Disciplines” and “Code
                  of Conduct for Students and Conflict Handling Procedure” at
                  http://www.sbcclny.com/school-policy-forms.
                </li>
                <li className="list-group-item">
                  Students are expected to be honest in completing all
                  school-related tests and homework assignments. Plagiarism is
                  not tolerated and will be treated seriously.
                </li>
                <li className="list-group-item">
                  No cell phones and electronics will be permitted at language
                  and enrichment classes unless explicitly requested by the
                  teacher for learning purposes.
                </li>
                <li className="list-group-item">
                  Students who fail to obey the school disciplines will be given
                  warnings. Serious cases may lead to suspension or dismissal
                  from the school. No tuition refund will be given if the
                  student is removed from school.
                </li>
              </ul>
            </li>
          </ol>
        </div>
        <div className="mx-auto btn-group pt-2">
          <input
            className="btn btn-primary active mr-2"
            type="button"
            value="Agree"
            onClick={() => {
              setWaitForResponse(true);
              signTerms(
                userInfo.auth,
                () => {
                  callback();
                  setWaitForResponse(false);
                },
                () => {
                  failureCallback();
                  setWaitForResponse(false);
                }
              );
            }}
            disabled={waitForResponse}
          />
          <input
            className="btn btn-secondary mr-2"
            type="button"
            value="Decline"
            onClick={() => {
              setWaitForResponse(true);
              failureCallback();
              setWaitForResponse(false);
            }}
            disabled={waitForResponse}
          />
        </div>
      </form>
    </div>
  );
}
