import React, { useReducer } from "react";

import UserMainPage from "../user/UserMainPage.tsx";
import UserFrontPage from "../user/UserFrontPage.tsx";

// Bootstrap CSS
import "bootstrap/dist/css/bootstrap.min.css";
// Bootstrap Bundle JS
import "bootstrap/dist/js/bootstrap.bundle.min";

// Some Hardcoded user information for development purpose. Read data will be loaded from the
// backend.
const Page = {
  StartLogin: 0, // User is on login page
  PostLogin: 1, // User successfully logged in, showing the user profile page.
};

const reducer = (user_repo, action) => {
  switch (action.type) {
    case "login_complete":
      return {
        ...user_repo,
        page: Page.PostLogin,
        user_info: action.user_info,
      };
    case "logout":
      return {
        ...user_repo,
        page: Page.StartLogin,
        user_info: action.user_info,
      };
    default:
      throw new Error("Unrecognized action type?");
  }
};

const INITIAL_STATE = {
  /* Default on login page*/
  page: Page.StartLogin,
  // Basic user information including
  // a. username, password
  // b. Auth token
  user_info: null,
};

export const UserContext = React.createContext([]);

const { Provider } = UserContext;

const App = () => {
  const [user_profile, transitionUserState] = useReducer(
    reducer,
    INITIAL_STATE
  );

  // Used by the UserFrontPage to passback the user information
  const loginSuccess = (userInfo) => {
    transitionUserState({
      type: "login_complete",
      user_info: userInfo,
    });
  };

  // Used by the UserMainPage to logout and switch to back to login page.
  const logOut = () => {
    transitionUserState({ type: "logout", user_info: null });
  };

  return (
    <div>
      <Provider value={[user_profile, transitionUserState]}>
        {user_profile.page === Page.StartLogin && (
          <UserFrontPage loginSuccessCallback={loginSuccess} />
        )}

        {user_profile.page === Page.PostLogin && (
          <UserMainPage
            userInfo={user_profile.user_info}
            logOutCallback={logOut}
          />
        )}
      </Provider>
    </div>
  );
};

export default App;
