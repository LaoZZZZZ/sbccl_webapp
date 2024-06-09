import axios from "axios";

export interface Payment {
  registration_code: number;
  pay_date: Date;
  original_amount: number;
  amount_in_dollar: number;
  payment_method: string;
  payment_status: string;
  last_udpate_date: Date;
}

export interface PaymentsResponse {
  errMsg: string;
  payments: Payment[];
}
/**
 *
 * @param user_auth: user authentication information for api call
 * @param callback: Client provided callback upon receiving response.
 * @returns
 */
export const FetchPayments = async (user_auth: {}, callback) => {
  await axios
    .get(
      process.env.REACT_APP_BE_URL_PREFIX + "/rest_api/members/fetch-payments/",
      {
        headers: {
          "Content-Type": "application/json",
        },
        auth: user_auth,
      }
    )
    .then((response) => {
      console.log(response);
      callback({
        errMsg: "",
        payments: response.data.payments.map(JSON.parse),
      });
    })
    .catch((error) => {
      callback({
        errMsg: error.response.data.detail,
        payments: null,
      });
    });
};
