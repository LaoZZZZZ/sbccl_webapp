import React, { useState } from "react";

interface Props {
  labelText: string;
  inputType: string;
  placeHolder?: string;
  requiredInput?: boolean;
  retrieveInput: (string) => void;
}
const TextInput = ({
  labelText,
  inputType,
  placeHolder,
  requiredInput,
  retrieveInput,
}: Props) => {
  const [errorMessage, setErrorMessage] = useState("");

  return (
    <>
      <label htmlFor="textInput" className="htmlForm-label">
        {labelText}
      </label>
      <input
        type={inputType}
        className="form-control"
        id={labelText}
        placeholder={placeHolder}
        required={requiredInput}
        onChange={(e) => {
          if (e.target.value == "") {
            setErrorMessage("Please enter " + labelText);
            retrieveInput("");
          } else {
            setErrorMessage("");
            retrieveInput(e.target.value);
          }
        }}
      />
      {requiredInput && errorMessage !== "" && (
        <div
          id={labelText + "warning"}
          className={errorMessage === "" ? "form-text" : "text-warning"}
        >
          {errorMessage}
        </div>
      )}
    </>
  );
};

export default TextInput;
