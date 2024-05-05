import axios from "axios";

/**
 *
 * @param user_info: user authentication information for api call
 * @param coupon: json format of coupon to be validated
 * @param callback:
 * @returns
 */
const GetCoupon = async (user_info, coupon, callback) => {
  await axios
    .get(
      process.env.REACT_APP_BE_URL_PREFIX +
        "/rest_api/members/coupon-details/" +
        coupon +
        "/",
      {
        headers: {
          "Content-Type": "application/json",
        },
        auth: {
          username: user_info.auth.username,
          password: user_info.auth.password,
        },
      }
    )
    .then((response) => {
      callback({ errMsg: "", coupon: JSON.parse(response.data) });
    })
    .catch((error) => {
      callback({ error_msg: error.response.data, coupon: null });
    });
};

export default GetCoupon;
