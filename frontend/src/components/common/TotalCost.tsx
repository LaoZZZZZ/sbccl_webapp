import React, {useState} from "react";
import validateCoupon from "./GetCoupon.tsx";

interface TotalCostProps {
  user_info: {};
  amount: any;
}

/**
 * Component that shows the total cost and coupon application if possible.
 */
const TotalCost = ({ user_info, amount }: TotalCostProps): JSX.Element => {
  const [couponCode, setCouponCode] = useState("");
  const [couponInfo, setCouponInfo] = useState({
    'error_msg': "", 'data': {}
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
                setCouponCode(e.target.value)
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
                validateCoupon(user_info, {'coupon_code': couponCode}, (response)=>{
                  if (response['data'] === null) {
                    setErrMsg(response['error_msg'])
                  }
                  setCouponInfo(response['data'])
                })
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
function useState(arg0: string): [any, any] {
  throw new Error("Function not implemented.");
}

