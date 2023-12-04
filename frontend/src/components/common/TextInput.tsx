import React, { useState } from "react";

interface Props {
  labelText: string;
  inputType: string;
  placeHolder?: string;
  requiredInput?: boolean;
}
const TextInput = ({
  labelText,
  inputType,
  placeHolder,
  requiredInput,
}: Props) => {
  const [errorMessage, setErrorMessage] = useState("");

  return (
    <div className="mb-3">
      <label htmlFor="examplehtmlFormControlInput1" className="htmlForm-label">
        {labelText}
      </label>
      <input
        type={inputType}
        className="form-control"
        id="exampleFormControlInput1"
        placeholder={placeHolder}
        required={requiredInput}
        onChange={(e) => {
          if (e.target.value == "") {
            setErrorMessage("Please enter " + labelText);
          } else {
            setErrorMessage("");
          }
        }}
      />
      {requiredInput && errorMessage !== "" && (
        <div
          id="textInputWarning"
          className={errorMessage === "" ? "form-text" : "text-warning"}
        >
          {errorMessage}
        </div>
      )}
    </div>
  );
};

export default TextInput;
