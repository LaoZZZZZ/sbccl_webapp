import React from "react";

interface TotalCostProps {
  amount: number;
}

/**
 * Component that shows the total cost and coupon application if possible.
 */
const TotalCost = ({ amount }: TotalCostProps) => {
  return (
    <div className="row g-3 align-items-left">
      <div className="col-auto">
        <label className="col-form-label">
          <strong>Total cost</strong>:
        </label>
      </div>
      <div className="col-auto">
        <label className="col-form-label">${amount}</label>
      </div>
    </div>
  );
};
// #endregion

export default TotalCost;
