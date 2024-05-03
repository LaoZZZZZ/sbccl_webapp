import React from "react";
import TextInput from "./TextInput.tsx";
// #region constants

// #endregion

// #region styled-components

// #endregion

// #region functions

// #endregion

// #region component
interface TotalCostProps {
  amount: any;
}

/**
 *
 */
const TotalCost = ({ amount }: TotalCostProps): JSX.Element => {
  return (
    <div className="form-group">
      <div className="form-group mb-2">
        <label className="sr-only" htmlFor="student">
          <strong>Total cost</strong>
        </label>
        <div className="row g-3">
          <div className="col-auto">
            <label className="form-control-plaintext" id="staticEmail2">
              {amount}
            </label>
          </div>
          <div className="col-auto">
            <input
              type="text"
              className="form-control col-auto"
              placeholder="Coupon Code"
              aria-label="Coupon"
            />
          </div>
          <div className="col-auto">
            <input
              type="button"
              className="btn btn-outline-primary col-auto"
              value="Apply"
              id="coupon-button"
            />
          </div>
        </div>
      </div>
    </div>
  );
};
// #endregion

export default TotalCost;
