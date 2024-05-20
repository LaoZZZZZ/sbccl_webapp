import React, { useEffect, useState } from "react";
import {
  FetchCalendar,
  FetchResponse,
  CalendarDate,
} from "../common/FetchCalendar.tsx";
import Calendar from "../common/Calendar.tsx";
import Alert from "../common/Alert.tsx";

interface CalendarDetailPageProps {
  userAuth: {};
}

/**
 *
 */
const CalendarDetailPage = ({ userAuth }: CalendarDetailPageProps) => {
  const [fetchDetail, setFetchDetail] = useState<FetchResponse>({
    errMsg: "",
    calendar: [],
  });

  const [fetched, setFetched] = useState(false);

  const handleFetchResponse = (response: FetchResponse) => {
    setFetchDetail(response);
    setFetched(true);
  };
  useEffect(() => {
    if (!fetched) {
      FetchCalendar(userAuth, handleFetchResponse);
    }
  }, [fetched]);

  return (
    <div>
      {fetched && fetchDetail?.errMsg !== "" && (
        <Alert
          success={false}
          message={fetchDetail.errMsg}
          parentCallback={() => {
            setFetchDetail({
              errMsg: "",
              calendar: [],
            });
            setFetched(true);
          }}
        />
      )}
      {fetched && fetchDetail?.errMsg === "" && (
        <Calendar schoolDates={fetchDetail.calendar} />
      )}
    </div>
  );
};
// #endregion

export default CalendarDetailPage;
