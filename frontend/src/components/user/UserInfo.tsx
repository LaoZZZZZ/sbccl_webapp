interface UserInfo {
  auth: {
    username: string;
    password: string;
  };

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
