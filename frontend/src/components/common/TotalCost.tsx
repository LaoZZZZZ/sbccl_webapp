import React, { useState } from "react";
import validateCoupon from "./GetCoupon.tsx";

interface TotalCostProps {
  user_info: {};
  amount: any;
}

interface Coupon {
  code: string;
  expiration_date: Date;
  reason: string;
  type: string;
  dollar_amount: string;
  percentage: string;
  application_rule: string;
}

// Json format for the data model of backend API call.
interface CouponDetails {
  errMsg: string;
  coupon: Coupon;
}

/**
 * Component that shows the total cost and coupon application if possible.
 */
const TotalCost = ({ user_info, amount }: TotalCostProps) => {
  const [couponCode, setCouponCode] = useState("");
  const [couponDetails, setCouponDetails] = useState<CouponDetails>({
    errMsg: "",
    coupon: {
      code: "",
      expiration_date: new Date(),
      reason: "",
      type: "",
      dollar_amount: "",
      percentage: "",
      application_rule: "",
    },
  });

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
              onChange={(e) => {
                setCouponCode(e.target.value);
              }}
            />
          </div>
          <div className="col-auto">
            <input
              type="button"
              className="btn btn-outline-primary col-auto"
              value="Apply"
              id="coupon-button"
              onClick={() => {
                validateCoupon(user_info, couponCode, setCouponDetails);
              }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};
// #endregion

export default TotalCost;
