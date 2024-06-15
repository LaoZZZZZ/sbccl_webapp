import React from "react";

export interface Dropout {
  id: number;
  course_name: string;
  student: number;
  school_year_start: Date;
  school_year_end: Date;
  original_registration_code: string;
}

// #region component
interface DropoutDetailsProps {}

/**
 *
 */
const DropoutDetails = ({}: DropoutDetailsProps): JSX.Element => {
  return <div></div>;
};
// #endregion

export default DropoutDetails;
