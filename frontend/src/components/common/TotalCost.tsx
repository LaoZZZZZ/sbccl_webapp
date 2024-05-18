import React from "react";

interface TotalCostProps {
  original_amount: number;
  updated_amount: number;
}

/**
 * Component that shows the total cost and coupon application if possible.
 */
const TotalCost = ({ original_amount, updated_amount }: TotalCostProps) => {
  const hasDiscount = original_amount > updated_amount;
  return (
    <div className="row g-2 align-items-left">
      <div className="col-auto">
        <label className="col-form-label">
          <strong>Total cost</strong>:
        </label>
      </div>
      <div className="col-auto">
        <label className="col-form-label">
          <p className={hasDiscount ? "text-success" : "text-primary"}>
            ${updated_amount}
            {hasDiscount && (
              <del className="text-secondary"> (${original_amount})</del>
            )}
          </p>
        </label>
      </div>
    </div>
  );
};
// #endregion

export default TotalCost;
