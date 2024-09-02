export interface Auth {
  username: string;
  password: string;
}

export interface UserDetails {
  username: string; // should hold the same value with email
  email: string;
  last_name: string;
  first_name: string;
  // possible value
  // 1. Parent
  // 2. Board Member
  // 3. Teacher
  // 4. Volunteer
  member_type: string;
  phone_number: string;
  last_login: Date;
  date_joined: Date;
  term_signed_date: Date;
}

export interface AccountInfo {
  auth: Auth;
  user: UserDetails;
}
