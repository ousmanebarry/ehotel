import axios from "axios";
import Cookies from "js-cookie";
import { useState } from "react";
import { Container } from "@mantine/core";
import { message } from "antd";
import Header from "~/components/Header";
import HotelForm from "~/components/HotelForm";
import { HotelInfo } from "~/types";

export default function AddHotel() {
  const [formReset, setFormReset] = useState(() => () => {});

  const handleSubmit = async (values: HotelInfo) => {
    try {
      const access_token = Cookies.get("access_token");

      await axios.post(
        "${process.env.NEXT_PUBLIC_URL}/hotel/hotel",
        {
          hotel_ID: values.hotel_id,
          chain_ID: values.chain_id,
          number_of_rooms: values.number_of_rooms,
          address_street_name: values.address_street_name,
          address_street_number: values.address_street_number,
          address_city: values.address_city,
          address_province_state: values.address_province_state,
          address_country: values.address_country,
          contact_email: values.contact_email,
          star_rating: values.star_rating,
        },
        {
          headers: { Authorization: `Bearer ${access_token}` },
        }
      );

      formReset();
      message.success("Hotel successfully created");
    } catch (error: any) {
      message.error(error.response.data.message);
    }
  };

  return (
    <>
      <Header />
      <main>
        <Container sx={{ marginTop: "20px", marginBottom: "20px" }} size="sm">
          <HotelForm onSubmit={handleSubmit} setFormReset={setFormReset} />
        </Container>
      </main>
    </>
  );
}
