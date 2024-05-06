import React from "react";

interface TotalCostProps {
  amount: number;
}

/**
 * Component that shows the total cost and coupon application if possible.
 */
const TotalCost = ({ amount }: TotalCostProps) => {
  return (
    <div className="form-group">
      <div className="form-group mb-2">
        <label className="sr-only" htmlFor="student">
          <strong>Total cost</strong>
        </label>
        <div className="col-auto">
          <label className="form-control-plaintext" id="staticEmail2">
            ${amount}
          </label>
        </div>
      </div>
    </div>
  );
};
// #endregion

export default TotalCost;
