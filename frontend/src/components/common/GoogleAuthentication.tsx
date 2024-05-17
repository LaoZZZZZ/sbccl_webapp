import { GoogleLogin, GoogleOAuthenProvider } from "@react-oauth/google";
import React from "react";

const GoogleAuthentication = ({
  original_amount,
  updated_amount,
}: TotalCostProps) => {
  return (
    <GoogleOAuthProvider clientId="YOUR CLIENT ID">
      <GoogleLogin onSuccess={handleLogin} />
    </GoogleOAuthProvider>
  );
};

export default GoogleAuthentication;
