import axios from "axios";
import { Auth } from "../user/UserInfo";

export enum BroadCastEvent {
  None = "None",
  AllParent = "AllParent",
  AllTeacher = "AllTeacher",
  AllTeachingAssistant = "AllTa",
}

export interface Notification {
  // If true, it's a broadcast message to all people
  broadcast: BroadCastEvent;
  // Id of the notification receiver, receipient is not used if all is true.
  recipient: number;
  subject: string;
  body: string;
}

//
export const sendNotification = async (
  userAuth: Auth,
  message: Notification,
  successCallback: () => void,
  failureCallback: (errMsg: string) => void
) => {
  await axios
    .put(
      process.env.REACT_APP_BE_URL_PREFIX +
        "/rest_api/members/send-notification/",
      { message },
      {
        auth: userAuth,
      }
    )
    .then((whatever_response) => {
      successCallback();
      return true;
    })
    .catch((error) => {
      failureCallback(error.response.data.detail);
      return false;
    });
};
