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
    <div className="md-3">
      <label htmlFor="textInput" className="col-sm-3 col-form-label">
        {completeLabel}
      </label>
      <input
        type={inputType}
        className="col-sm-3 col-form-label"
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
    </div>
  );
};

export default TextInput;
