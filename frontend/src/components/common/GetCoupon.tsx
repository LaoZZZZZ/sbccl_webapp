import axios from "axios";

/**
 * 
 * @param user_info: user authentication information for api call
 * @param coupon: json format of coupon to be validated
 * @param callback:  
 * @returns 
 */
const GetCoupon = async (user_info, coupon, callback) => {
  const response = await axios.get(
    process.env.REACT_APP_BE_URL_PREFIX + "/rest_api/members/get-coupon",
    {
      headers: {
        "Content-Type": "application/json",
      },
      coupon,
      auth: {
        username: user_info.auth.username,
        password: user_info.auth.password,
      },
    }
  );

  if (response.status === 200) {
    callback({'data': JSON.parse(response.data)});
    return;
  }

  callback({'error_msg': response.data});
};

export default GetCoupon;
