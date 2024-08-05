export interface Auth {
  username: string;
  password: string;
}

export interface UserDetails {
  username: string; // should hold the same value with email
  email: string;
  last_name: string;
  first_name: string;
  member_type: string;
  phone_number: string;
  last_login: Date;
  date_joined: Date;
}

export interface AccountInfo {
  auth: Auth;
  user: UserDetails;
}
