import React, { useState } from "react";

interface Props {
  title: string; // Title of the modal
  bodyMsg: string; // what's on the message in the modal
  callBackUponConfirm: () => {};
  dismissCallback: () => {};
}

const ModelWindow = ({
  title,
  bodyMsg,
  callBackUponConfirm,
  dismissCallback,
}: Props) => {
  return (
    <div className="modal-show" tabIndex={-1} id={title} role="dialog">
      <div className="modal-dialog-centered" role="document">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">{title}</h5>
          </div>
          <div className="modal-body">
            <p>{bodyMsg}</p>
          </div>
          <div className="modal-footer">
            <button
              type="button"
              className="btn btn-primary"
              onClick={() => {
                callBackUponConfirm();
              }}
            >
              Confirm
            </button>
            <button
              type="button"
              className="btn btn-secondary"
              data-dismiss="modal"
              onClick={() => {
                dismissCallback();
              }}
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModelWindow;
