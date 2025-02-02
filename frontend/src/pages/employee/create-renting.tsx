import axios from "axios";
import dayjs from "dayjs";
import Cookies from "js-cookie";
import { useState } from "react";
import { Container } from "@mantine/core";
import { message } from "antd";
import Header from "~/components/Header";
import RentingForm from "~/components/RentingForm";
import useToken from "~/utils/useToken";
import { RentingFormInfo, RoomInfo } from "~/types";

export default function CreateRenting() {
  const [formReset, setFormReset] = useState(() => () => {});
  const token = useToken();

  const handleSubmit = async (values: RentingFormInfo) => {
    try {
      const check_in = dayjs(values.check_in_date, "YYYY-MM-DD");
      const check_out = dayjs(values.check_out_date, "YYYY-MM-DD");
      const stay_duration = check_out.diff(check_in, "days");
      const { data: room } = await axios.get<RoomInfo>(
        `${process.env.NEXT_PUBLIC_URL}/room/room/${values.hotel_ID}/${values.room_number}`
      );

      const access_token = Cookies.get("access_token");

      const { data } = await axios.get<{ employee_ID: number }>(
        `${process.env.NEXT_PUBLIC_URL}/auth/employees/${token.user_ssn_sin}`,
        {
          headers: { Authorization: `Bearer ${access_token}` },
        }
      );

      await axios.post(
        `${process.env.NEXT_PUBLIC_URL}/rental/rental`,
        {
          ...values,
          employee_ID: data.employee_ID,
          total_paid:
            stay_duration * room.price_per_night * (1 - values.discount / 100) +
            values.additional_charges,
        },
        {
          headers: { Authorization: `Bearer ${access_token}` },
        }
      );

      formReset();
      message.success("Renting successfully created");
    } catch (error: any) {
      message.error(error.response.data.message);
    }
  };

  return (
    <>
      <Header />
      <main>
        <Container sx={{ marginTop: "20px", marginBottom: "20px" }} size="xs">
          <RentingForm onSubmit={handleSubmit} setFormReset={setFormReset} />
        </Container>
      </main>
    </>
  );
}
