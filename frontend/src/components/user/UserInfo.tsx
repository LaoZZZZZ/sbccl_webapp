export interface Auth {
  username: string;
  password: string;
}

interface UserInfo {
  auth: Auth;

  user: {
    username: string; // should hold the same value with email
    email: string;
    last_name: string;
    first_name: string;
    member_type: string;
    phone_number: string;
    last_login: Date;
    date_joined: Date;
  };
}

export default UserInfo;
