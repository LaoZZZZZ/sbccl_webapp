import React from "react";
import cclBanner from "../../resource/banner.jpg";

const PageHead = () => {
  return (
    <div className="container-xxl">
      <div className="row">
        <div className="col top-0 start-0 opacity-75">
          <img src={cclBanner} alt="CCL"></img>
        </div>
        <div className="col justify-content-md-left">
          <a href="https://www.sbcclny.com.">Sbccl Page</a>
          <button type="button" className="btn btn-link">
            Profile
          </button>
          <button type="button" className="btn btn-link">
            Logout
          </button>
        </div>
      </div>
    </div>
  );
};

export default PageHead;
