import React from "react";

interface Props {
  class_name: string;
  teachers_info: [];
  exitCallBack: () => {};
}

const AccountDetail = ({ class_name, teachers_info, exitCallBack }: Props) => {
  const table_columns_names = ["Last Name", "First Name", "Email"];
  const keys = ["last_name", "first_name", "email"];
  return (
    <>
      <div className="col-auto btn-group">
        <button
          type="button"
          className="btn btn-outline-primary position-relative start-200"
          onClick={() => {
            exitCallBack();
          }}
        >
          Go back
        </button>
      </div>
      <hr className="pb-2" />

      <div className="table-responsive">
        <table className="table table-bordered table-hover table-striped">
          <caption>Teachers for {class_name}</caption>
          <thead>
            <tr id="column_name">
              {table_columns_names.map((colmunName) => {
                return <th scope="col">{colmunName}</th>;
              })}
            </tr>
          </thead>
          <tbody>
            {teachers_info.map((teacher) => (
              <tr>
                {keys.map((column) => {
                  return <td> {teacher[column]}</td>;
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
};

export default AccountDetail;
