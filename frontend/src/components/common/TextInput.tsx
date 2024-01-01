import React, { useState } from "react";

interface Props {
  labelText: string;
  inputType: string;
  placeHolder?: string;
  requiredInput?: boolean;
  retrieveInput: (string) => void;
  // returns true if the value is valid.
  validationFunc: (string) => boolean;
}
const TextInput = ({
  labelText,
  inputType,
  placeHolder,
  requiredInput,
  retrieveInput,
  validationFunc,
}: Props) => {
  const [errorMessage, setErrorMessage] = useState("");
  const completeLabel = (requiredInput ? "*" : "").concat(labelText);
  return (
    <>
      <label htmlFor="textInput" className="htmlForm-label">
        {completeLabel}
      </label>
      <input
        type={inputType}
        className="form-control"
        id={labelText}
        placeholder={placeHolder}
        required={requiredInput}
        onChange={(e) => {
          if (!validationFunc(e.target.value)) {
            setErrorMessage("Please provide valid " + labelText);
            retrieveInput("");
            return;
          }
          setErrorMessage("");
          retrieveInput(e.target.value);
        }}
      />
      {errorMessage !== "" && (
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
