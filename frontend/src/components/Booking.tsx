import axios from "axios";
import dayjs from "dayjs";
import Cookies from "js-cookie";
import { useState } from "react";
import { useDisclosure } from "@mantine/hooks";
import { Text, Stack, Button, Group, Paper } from "@mantine/core";
import { message } from "antd";
import AddPaymentInfo from "~/components/AddPaymentInfo";
import useToken from "~/utils/useToken";
import { BookingInfo, RoomInfo } from "~/types";

interface BookingProps {
  booking: BookingInfo;
}

export default function Booking({ booking }: BookingProps) {
  const token = useToken();

  const [added, { open: add }] = useDisclosure();
  const [display, setDisplay] = useState(true);

  const handleCancel = async () => {
    try {
      const access_token = Cookies.get("access_token");
      await axios.delete(
        `${process.env.NEXT_PUBLIC_URL}/booking/booking/${booking.booking_ID}`,
        { headers: { Authorization: `Bearer ${access_token}` } }
      );

      setDisplay(false);
      message.success("Booking successfully cancelled");
    } catch {
      message.error("Something went wrong while trying to cancel the booking");
    }
  };

  const handleConvertToRenting = async () => {
    try {
      const check_in = dayjs(booking.scheduled_check_in_date, "YYYY-MM-DD");
      const check_out = dayjs(booking.scheduled_check_out_date, "YYYY-MM-DD");
      const stay_duration = check_out.diff(check_in, "days");
      const { data: room } = await axios.get<RoomInfo>(
        `${process.env.NEXT_PUBLIC_URL}/room/room/${booking.hotel_ID}/${booking.room_number}`
      );

      const access_token = Cookies.get("access_token");
      const { data } = await axios.get<{ employee_ID: number }>(
        `${process.env.NEXT_PUBLIC_URL}/auth/employees/${token.user_ssn_sin}`,
        {
          headers: { Authorization: `Bearer ${access_token}` },
        }
      );

      await axios.post(
        `${process.env.NEXT_PUBLIC_URL}/rental/rental/convert/${booking.booking_ID}`,
        {
          total_paid: stay_duration * room.price_per_night,
          discount: 0,
          additional_charges: 0,
          employee_id: data.employee_ID,
        },
        { headers: { Authorization: `Bearer ${access_token}` } }
      );

      setDisplay(false);
      message.success("Booking successfully converted to a renting");
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
            <Text fw="bold">Booked:</Text>
            {booking.booking_date}
          </Text>
          <Text align="right">
            <Text fw="bold">Customer Id:</Text>
            {booking.customer_SSN_SIN}
          </Text>
        </Group>
        <Group position="apart">
          <Text>
            <Text fw="bold">Hotel Id:</Text>
            {booking.hotel_ID}
          </Text>
          <Text align="right">
            <Text fw="bold">Room:</Text>
            {booking.room_number}
          </Text>
        </Group>
        <Group position="apart">
          <Text>
            <Text fw="bold">Check in:</Text>
            {booking.scheduled_check_in_date}
          </Text>
          <Text align="right">
            <Text fw="bold">Check out:</Text>
            {booking.scheduled_check_out_date}
          </Text>
        </Group>
        {token.role === "customer" && !booking.canceled && (
          <Button onClick={handleCancel}>Cancel</Button>
        )}
        {token.role === "employee" && (
          <Group position="apart">
            <AddPaymentInfo complete={added} setComplete={add} />
            <Button disabled={!added} onClick={handleConvertToRenting}>
              Convert To Renting
            </Button>
          </Group>
        )}
      </Stack>
    </Paper>
  );
}
