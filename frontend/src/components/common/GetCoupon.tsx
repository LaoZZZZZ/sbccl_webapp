import axios from "axios";

interface Coupon {
  code: string;
  expiration_date: Date;
  reason: string;
  type: string;
  dollar_amount: number;
  percentage: number;
  application_rule: string;
}

/**
 *
 * @param user_auth: user authentication information for api call
 * @param coupon: json format of coupon to be validated
 * @param callback:
 * @returns
 */
const GetCoupon = async (user_auth, coupon_code, original_amount, callback) => {
  const ApplyCoupon = (amount: number, coupon: Coupon) => {
    if (coupon.type === "A") {
      return Math.max(0, amount - coupon.dollar_amount);
    } else if (coupon.type === "P") {
      return (amount * (100 - coupon.percentage)) / 100.0;
    }
    return amount;
  };

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
      callback(ApplyCoupon(original_amount, JSON.parse(response.data)));
      return;
    })
    .catch((error) => {
      callback(original_amount);
    });
};

export default GetCoupon;
