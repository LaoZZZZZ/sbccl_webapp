import axios from "axios";

export interface Coupon {
  code: string;
  expiration_date: Date;
  reason: string;
  type: string;
  dollar_amount: number;
  percentage: number;
  application_rule: string;
}

export interface CouponResponse {
  errMsg: string;
  coupontDetails: Coupon;
}
/**
 *
 * @param user_auth: user authentication information for api call
 * @param coupon: json format of coupon to be validated
 * @param callback:
 * @returns
 */
export const GetCoupon = async (
  user_auth: {},
  coupon_code: string,
  callback
) => {
  await axios
    .get(
      process.env.REACT_APP_BE_URL_PREFIX +
        "/rest_api/members/" +
        coupon_code +
        "/coupon-details/",
      {
        headers: {
          "Content-Type": "application/json",
        },
        auth: user_auth,
      }
    )
    .then((response) => {
      callback({
        errMsg: "",
        couponDetails: JSON.parse(response.data),
      });
      return;
    })
    .catch((error) => {
      callback({
        errMsg: error.response.data.detail,
        couponDetails: null,
      });
    });
};
