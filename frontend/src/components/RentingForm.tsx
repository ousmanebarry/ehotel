import { useEffect, useCallback } from "react";
import { useDisclosure } from "@mantine/hooks";
import { useForm, isNotEmpty, isInRange } from "@mantine/form";
import {
  Button,
  Stack,
  Group,
  NumberInput,
  Text,
  Center,
  Box,
} from "@mantine/core";
import DateRangePicker from "~/components/DateRangePicker";
import AddPaymentInfo from "./AddPaymentInfo";
import { RentingFormInfo } from "~/types";

interface HotelForm {
  setFormReset?: (formReset: () => void) => void;
  onSubmit: (hotel: RentingFormInfo) => void;
}

export default function RentingForm(props: HotelForm) {
  const [opened, { open, close }] = useDisclosure();

  const form = useForm({
    initialValues: {
      discount: 0,
      additional_charges: 0,
      hotel_ID: null,
      room_number: null,
      customer_SSN_SIN: null,
      check_in_date: "",
      check_out_date: "",
    },
    validate: {
      discount: isInRange(
        { min: 0, max: 100 },
        "Discount must be between 0 to 100"
      ),
      additional_charges: isInRange(
        { min: 0 },
        "Additional charges must be positive"
      ),
      hotel_ID: isNotEmpty("Provide a hotel id"),
      room_number: isNotEmpty("Provide a room number"),
      customer_SSN_SIN: isNotEmpty("Provide customer SSN"),
      check_in_date: isNotEmpty("Select check in and check out dates"),
      check_out_date: isNotEmpty("Select check in and check out dates"),
    },
  });

  const handleDateChange = useCallback(
    (dateRange: string[]) => {
      form.setValues({
        check_in_date: dateRange[0],
        check_out_date: dateRange[1],
      });
    },
    [form.setValues]
  );

  useEffect(() => {
    if (props.setFormReset) props.setFormReset(() => form.reset);
  }, [form.reset, props.setFormReset]);

  return (
    <Stack spacing="md">
      <NumberInput
        placeholder="Customer SSN"
        label="Customer SSN"
        {...form.getInputProps("customer_SSN_SIN")}
      />
      <Group position="apart">
        <NumberInput
          placeholder="Hotel Id"
          label="Hotel Id"
          {...form.getInputProps("hotel_ID")}
        />
        <NumberInput
          placeholder="Room number"
          label="Room number"
          {...form.getInputProps("room_number")}
        />
      </Group>
      <Group position="apart">
        <NumberInput
          placeholder="Discount"
          icon="%"
          label="Discount"
          {...form.getInputProps("discount")}
          sx={{ maxWidth: "225px" }}
        />
        <NumberInput
          placeholder="Additional Charges"
          icon="$"
          label="Additional Charges"
          {...form.getInputProps("additional_charges")}
          sx={{ maxWidth: "225px" }}
        />
      </Group>
      <Center>
        <Stack sx={{ padding: "10px 0px" }}>
          <DateRangePicker
            setDateRange={handleDateChange}
            startDateLabel="Check In"
            endDateLabel="Check Out"
          />
          <Text color="red" size="xs" sx={{ marginTop: "-10px" }}>
            {form.errors.check_in_date}
          </Text>
        </Stack>
      </Center>
      <Group position="apart">
        <AddPaymentInfo complete={opened} setComplete={open} />
        <Button
          type="submit"
          onClick={form.onSubmit(props.onSubmit as any) as any}
          disabled={!opened}
        >
          Submit
        </Button>
      </Group>
    </Stack>
  );
}
