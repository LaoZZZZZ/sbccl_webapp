import axios from "axios";
import { Student } from "../user/FetchStudents";
import { Course } from "../user/FetchCourses.tsx";
import { Coupon } from "./GetCoupon.tsx";
import { Payment } from "./FetchPayments.tsx";

export interface Registration {
  id: number;
  course_name: string;
  student: number;
  school_year_start: Date;
  school_year_end: Date;
  original_registration_code: string;
  on_waiting_list: boolean;
}

export interface RegistrationBundle {
  student: Student;
  registration: Registration;
  course: Course;
  coupons: Coupon[];
  teacher: [];
  payments: Payment;
  balance: number;
}

export interface Registrations {
  errMsg: string;
  dropouts: RegistrationBundle[];
}

const fetchRegistrations = async (user_info, callback) => {
  const response = await axios.get(
    process.env.REACT_APP_BE_URL_PREFIX +
      "/rest_api/members/list-registrations",
    {
      headers: {
        "Content-Type": "application/json",
      },
      auth: {
        username: user_info.auth.username,
        password: user_info.auth.password,
      },
    }
  );

  if (response.status === 200) {
    const registrations = response.data.registrations.map(JSON.parse);
    callback({
      fetched: true,
      value: registrations,
    });
    return;
  }
  callback({ fetched: true, value: [] });
};

export default fetchRegistrations;
