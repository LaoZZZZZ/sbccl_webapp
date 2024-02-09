import "bootstrap/dist/css/bootstrap.css";
import React from "react";
import ReactDOM from "react-dom/client";
import ErrorPage from "./error-page.jsx";
import App from "./components/app/App.tsx";
import VerifyUser from "./components/user/VerifyUser.tsx";
import reportWebVitals from "./reportWebVitals";
import { redirect } from "react-router-dom";

import {
  Route,
  createBrowserRouter,
  createRoutesFromElements,
  RouterProvider,
} from "react-router-dom";
import ResetPasswordByCode from "./components/user/ResetPasswordByCodePage.tsx";

const router = createBrowserRouter(
  createRoutesFromElements([
    <Route path="/" element={<App />} errorElement={<ErrorPage />} />,
    <Route path="/login" element={<App />} errorElement={<ErrorPage />} />,
    <Route
      path="/verify-user/:verification_code"
      element={<VerifyUser />}
      errorElement={<ErrorPage />}
    />,
    <Route
      path="/reset-password-by-code/:verification_code"
      element={<ResetPasswordByCode />}
      errorElement={<ErrorPage />}
    />,
  ])
);

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
