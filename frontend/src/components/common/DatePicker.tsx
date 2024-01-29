import React, { useState } from "react";

interface Props {
  requiredInput?: boolean;
  retrieveInput: (string) => void;
}

// Calculate the latest acceptable DoB.
// The student must be at least 4.5 years old to attend the school
const getLatestDobMonthAndYear = () => {
  const current_year = new Date().getFullYear() - 4;
  return current_year.toString() + "-03-01";
};

const isDoBValid = (dobString) => {
  const dob = new Date(dobString);
  const acceptedDob = new Date(getLatestDobMonthAndYear());
  // otherwise the student is too yong to be added.
  return acceptedDob - dob >= 0;
};

const DatePicker = ({ requiredInput, retrieveInput }: Props) => {
  const labelString: string = "Date of Birth";
  const [errorMessage, setErrorMessage] = useState("");
  const completeLabel = (requiredInput ? "*" : "").concat(labelString);
  return (
    <div className="pb-2">
      <label htmlFor="textInput">{completeLabel}</label>
      <input
        type="date"
        className="form-control"
        id="dob"
        required={requiredInput}
        onChange={(e) => {
          if (!isDoBValid(e.target.value)) {
            setErrorMessage(
              "The child is too yong to attend Chinese school. The date of birth must be before " +
                getLatestDobMonthAndYear()
            );
            retrieveInput("");
            return;
          }
          setErrorMessage("");
          retrieveInput(e.target.value);
        }}
      />
      {errorMessage !== "" && (
        <div
          id={labelString + "warning"}
          className={errorMessage === "" ? "form-text" : "text-danger"}
        >
          {errorMessage}
        </div>
      )}
    </div>
  );
};

export default DatePicker;
