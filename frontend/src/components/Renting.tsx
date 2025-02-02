import { Text, Stack, Group, Paper } from "@mantine/core";
import { RentingInfo } from "~/types";

interface RentingProps {
  renting: RentingInfo;
}

export default function Renting({ renting }: RentingProps) {
  return (
    <Paper shadow="xs" p="lg" sx={{ width: "400px" }}>
      <Stack spacing="md">
        <Group position="apart">
          <Text>
            <Text fw="bold">Hotel Id:</Text>
            {renting.hotel_ID}
          </Text>
          <Text align="right">
            <Text fw="bold">Room Number:</Text>
            {renting.room_number}
          </Text>
        </Group>
        <Group position="apart">
          <Text>
            <Text fw="bold">Total Paid:</Text>
            {renting.total_paid}$
          </Text>
          <Text align="right">
            <Text fw="bold">Date Paid:</Text>
            {renting.date_paid}
          </Text>
        </Group>
        <Group position="apart">
          <Text>
            <Text fw="bold">Discount:</Text>
            {renting.discount}%
          </Text>
          <Text align="right">
            <Text fw="bold">Additional Charges:</Text>
            {renting.date_paid}$
          </Text>
        </Group>
        <Group position="apart">
          <Text>
            <Text fw="bold">Check In:</Text>
            {renting.check_in_date}
          </Text>
          <Text>
            <Text fw="bold">Check Out:</Text>
            {renting.check_out_date}
          </Text>
        </Group>
      </Stack>
    </Paper>
  );
}
