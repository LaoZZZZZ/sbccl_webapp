import "bootstrap/dist/css/bootstrap.css";
import React from "react";
import ReactDOM from "react-dom/client";
import ErrorPage from "./error-page.jsx";
import App from "./components/app/App.tsx";
import VerifyUser from "./components/user/VerifyUser.tsx";
import reportWebVitals from "./reportWebVitals";

import {
  Route,
  createBrowserRouter,
  createRoutesFromElements,
  RouterProvider,
} from "react-router-dom";
import { element } from "prop-types";

const router = createBrowserRouter(
  createRoutesFromElements([
    <Route path="/" element={<App />} errorElement={<ErrorPage />} />,
    <Route path="/login" element={<App />} errorElement={<ErrorPage />} />,
    <Route
      path="/verify-user/:verification_code"
      element={<VerifyUser />}
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
