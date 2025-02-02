import axios from "axios";
import Cookies from "js-cookie";
import { useState } from "react";
import { Container } from "@mantine/core";
import { message } from "antd";
import Header from "~/components/Header";
import RoomForm from "~/components/RoomForm";
import { RoomInfo } from "~/types";

export default function AddRoom() {
  const [formReset, setFormReset] = useState(() => () => {});

  const handleSubmit = async (values: RoomInfo) => {
    try {
      const access_token = Cookies.get("access_token");

      await axios.post(
        `${process.env.NEXT_PUBLIC_URL}/room/room`,
        {
          room_number: values.room_number,
          hotel_ID: values.hotel_id,
          room_capacity: values.room_capacity,
          view_type: values.view_type,
          price_per_night: values.price_per_night,
          is_extendable: values.is_extendable,
          room_problems: values.room_problems,
        },
        {
          headers: { Authorization: `Bearer ${access_token}` },
        }
      );

      formReset();
      message.success("Room successfully created");
    } catch (error: any) {
      message.error(error.response.data.message);
    }
  };

  return (
    <>
      <Header />
      <main>
        <Container sx={{ marginTop: "20px", marginBottom: "20px" }} size="sm">
          <RoomForm onSubmit={handleSubmit} setFormReset={setFormReset} />
        </Container>
      </main>
    </>
  );
}
