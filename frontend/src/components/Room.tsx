import axios from "axios";
import { useState, useEffect } from "react";
import Cookies from "js-cookie";
import { useDisclosure } from "@mantine/hooks";
import {
  Paper,
  Text,
  Group,
  Rating,
  Modal,
  Stack,
  Button,
  Box,
} from "@mantine/core";
import { message } from "antd";
import RoomForm from "~/components/RoomForm";
import useSearchQuery from "~/utils/useSearchQuery";
import useToken from "~/utils/useToken";
import { RoomInfo, HotelInfo, HotelChainInfo } from "~/types";

interface RoomProps {
  room: RoomInfo;
  hotel: HotelInfo;
  hotelChains: HotelChainInfo[];
}

export default function Room(props: RoomProps) {
  const [opened, { open, close }] = useDisclosure();
  //   const [hotel, setHotel] = useState<HotelInfo | null>();
  const [room, setRoom] = useState(props.room);
  const [display, setDisplay] = useState(true);
  const [startDate, endDate] = useSearchQuery((state) => [
    state.startDate,
    state.endDate,
  ]);

  const token = useToken();

  //   useEffect(() => {
  //     axios
  //       .get<HotelInfo>(
  //         `http://127.0.0.1:5000/hotel/hotel/${props.room.hotel_id}`
  //       )
  //       .then((res) => {
  //         const { data } = res;
  //         setHotel(data);
  //       });
  //   }, [props.room.hotel_id]);

  const handleDelete = async () => {
    try {
      const access_token = Cookies.get("access_token");

      await axios.delete(
        `${process.env.NEXT_PUBLIC_URL}/room/room/${props.hotel.hotel_ID}/${props.room.room_number}`,
        { headers: { Authorization: `Bearer ${access_token}` } }
      );

      setDisplay(false);
      message.success("Room successfully deleted");
    } catch (error: any) {
      message.error(error.response.data.message);
    }
  };

  const handleBooking = async () => {
    try {
      const access_token = Cookies.get("access_token");

      await axios.post(
        `${process.env.NEXT_PUBLIC_URL}/booking/booking`,
        {
          hotel_ID: props.hotel.hotel_ID,
          room_number: props.room.room_number,
          scheduled_check_in_date: startDate,
          scheduled_check_out_date: endDate,
        },
        { headers: { Authorization: `Bearer ${access_token}` } }
      );

      setDisplay(false);
      message.success("Room successfully booked");
    } catch (error: any) {
      message.error(error.response.data.message);
    }
  };

  const handleUpdate = async (values: RoomInfo) => {
    try {
      const access_token = Cookies.get("access_token");

      await axios.put(
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
        { headers: { Authorization: `Bearer ${access_token}` } }
      );

      close();
      setRoom({ ...room, ...values });
    } catch (error: any) {
      message.error(error.response.data.message);
    }
  };

  if (!display) return <></>;

  return (
    <Paper shadow="xs" p="lg" sx={{ width: "400px" }}>
      <Stack spacing="sm">
        <Group position="apart">
          <Text size="lg" weight={500}>
            <Text fw="bold">Room Number:</Text>
            {room.room_number}
          </Text>
          <Text align="right">
            <Text fw="bold">Hotel Id:</Text>
            {props.hotel.hotel_ID}
          </Text>
        </Group>
        <Group position="apart">
          <Text>
            <Text fw="bold">Hotel Chain:</Text>
            {
              props.hotelChains.find(
                (hotelChain) => hotelChain.chain_ID === props.hotel.chain_id
              )?.name
            }
          </Text>

          <Text align="right">
            <Text fw="bold">Star Rating:</Text>
            <Rating value={props.hotel.star_rating} readOnly />
          </Text>
        </Group>
        <Group position="apart" mt="sm">
          <Text>
            <Text fw="bold">Address:</Text>
            {`${props.hotel.address_street_number} ${props.hotel.address_street_name}, ${props.hotel.address_city}`}
          </Text>
          <Text align="right">
            <Text fw="bold">Location:</Text>
            {`${props.hotel.address_province_state}, ${props.hotel.address_country}`}
          </Text>
        </Group>

        <Group position="apart" mt="sm">
          <Text>
            <Text fw="bold">Room Capacity:</Text>
            {room.room_capacity}
          </Text>

          <Text align="right">
            <Text fw="bold">Price Per Night:</Text>${room.price_per_night}
          </Text>
        </Group>

        <Group position="apart" mt="sm">
          <Text>
            <Text fw="bold">View Type:</Text>
            {room.view_type}
          </Text>

          <Text align="right">
            <Text fw="bold">Is Extendable:</Text>
            {room.is_extendable ? "Yes" : "No"}
          </Text>
        </Group>
        {token.role === "customer" && (
          <Button
            size="md"
            compact
            onClick={handleBooking}
            disabled={!startDate && !endDate}
          >
            Book Now
          </Button>
        )}
        {token.role === "employee" && (
          <Group position="apart">
            <Button size="md" compact onClick={handleDelete}>
              Delete
            </Button>
            <Button size="md" compact onClick={open}>
              Edit
            </Button>
          </Group>
        )}
      </Stack>

      <Modal opened={opened} onClose={close} title="Edit Room">
        <Box sx={{ padding: "40px" }}>
          <RoomForm room={props.room} onSubmit={handleUpdate} />
        </Box>
      </Modal>
    </Paper>
  );
}
