import axios from "axios";
import Cookies from "js-cookie";
import { useState } from "react";
import { useDisclosure } from "@mantine/hooks";
import {
  Text,
  Stack,
  Button,
  Group,
  Paper,
  Modal,
  Rating,
} from "@mantine/core";
import { message } from "antd";
import HotelForm from "~/components/HotelForm";
import useToken from "~/utils/useToken";
import { HotelInfo } from "~/types";

interface HotelProps {
  hotel: HotelInfo;
}

export default function Hotel(props: HotelProps) {
  const [opened, { open, close }] = useDisclosure();
  const [display, setDisplay] = useState(true);
  const [hotel, setHotel] = useState(props.hotel);

  const token = useToken();

  const handleUpdate = async (values: HotelInfo) => {
    try {
      const access_token = Cookies.get("access_token");

      await axios.put(
        `${process.env.NEXT_PUBLIC_URL}/hotel/hotel`,
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

      close();
      setHotel({ ...hotel, ...values });
    } catch (error: any) {
      message.error(error.response.data.message);
    }
  };

  const handleDelete = async () => {
    try {
      const access_token = Cookies.get("access_token");

      await axios.delete(
        `${process.env.NEXT_PUBLIC_URL}/hotel/hotel/${props.hotel.hotel_id}`,
        { headers: { Authorization: `Bearer ${access_token}` } }
      );

      setDisplay(false);
      message.success("Successfully deleted hotel");
    } catch (error: any) {
      message.error(error.response.data.message);
    }
  };

  if (!display) return <></>;

  return (
    <Paper shadow="xs" p="lg" sx={{ width: "400px" }}>
      <Stack spacing="md">
        <Group position="apart">
          <Text>
            <Text fw="bold">Hotel ID:</Text> {hotel.hotel_id}
          </Text>
          <Text align="right">
            <Text fw="bold">Chain ID:</Text> {hotel.chain_id}
          </Text>
        </Group>
        <Group position="apart">
          <Text>
            <Text fw="bold">Number of Rooms:</Text>
            {hotel.number_of_rooms}
          </Text>
          <Text align="right">
            <Text fw="bold">Rating:</Text>
            <Rating value={hotel.star_rating} readOnly />
          </Text>
        </Group>
        <Group position="apart">
          <Text>
            <Text fw="bold">Street Name:</Text>
            {hotel.address_street_name}
          </Text>
          <Text align="right">
            <Text fw="bold">Street Number:</Text>
            {hotel.address_street_number}
          </Text>
        </Group>
        <Text>
          <Text fw="bold">City:</Text> {hotel.address_city}
        </Text>
        <Group position="apart">
          <Text>
            <Text fw="bold">Region:</Text>
            {hotel.address_province_state}
          </Text>
          <Text align="right">
            <Text fw="bold">Country:</Text> {hotel.address_country}
          </Text>
        </Group>

        {token.role === "employee" && (
          <Group position="apart">
            <Button onClick={handleDelete}>Delete</Button>
            <Button onClick={open}>Edit</Button>
          </Group>
        )}
      </Stack>

      <Modal opened={opened} onClose={close} title="Edit Hotel">
        <HotelForm hotel={hotel} onSubmit={handleUpdate} />
      </Modal>
    </Paper>
  );
}
