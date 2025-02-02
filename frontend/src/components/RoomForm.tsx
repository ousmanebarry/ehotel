import { useEffect } from "react";
import { useForm, isNotEmpty, isInRange } from "@mantine/form";
import {
  TextInput,
  Button,
  Text,
  Stack,
  Group,
  Radio,
  Textarea,
  Flex,
  SegmentedControl,
  NumberInput,
} from "@mantine/core";
import { RoomInfo } from "~/types";

interface RoomFormProps {
  room?: RoomInfo;
  setFormReset?: (formReset: () => void) => void;
  onSubmit: (room: RoomInfo) => void;
}

export default function RoomForm(props: RoomFormProps) {
  const form = useForm({
    initialValues: {
      room_number: props.room?.room_number || null,
      hotel_id: props.room?.hotel_ID || null,
      room_capacity: props.room?.room_capacity
        ? `${props.room.room_capacity}`
        : "1",
      view_type: props.room?.view_type || "",
      price_per_night: props.room?.price_per_night || null,
      is_extendable: props.room?.is_extendable ? "yes" : "no",
      room_problems: props.room?.room_problems || "",
    },
    validate: {
      room_number: isNotEmpty("Enter the room number"),
      hotel_id: isNotEmpty("Enter the hotel id"),
      room_capacity: isNotEmpty("Enter the room capacity"),
      view_type: isNotEmpty("Enter the view type"),
      price_per_night: isInRange({ min: 0 }, "Price must be positive"),
      room_problems: isNotEmpty("Enter the room problems"),
    },
    transformValues(values) {
      return {
        ...values,
        room_capacity: parseInt(values.room_capacity || "1"),
        is_extendable: values.is_extendable === "yes",
      };
    },
  });

  useEffect(() => {
    if (props.setFormReset)
      props.setFormReset(() => () => {
        form.setValues({
          room_number: null,
          hotel_id: null,
          room_capacity: "1",
          view_type: "",
          price_per_night: null,
          is_extendable: "no",
          room_problems: "",
        });
      });
  }, [form.reset, props.setFormReset]);

  return (
    <Stack spacing="md">
      {!props.room && (
        <Group>
          <NumberInput
            placeholder="Hotel Id"
            label="Hotel Id"
            {...form.getInputProps("hotel_id")}
          />
          <NumberInput
            placeholder="Room Number"
            label="Room Number"
            {...form.getInputProps("room_number")}
          />
        </Group>
      )}
      <NumberInput
        placeholder="Price Per Night"
        label="Price Per Night"
        icon="$"
        {...form.getInputProps("price_per_night")}
      />
      <TextInput
        placeholder="View Type"
        label="View Type"
        {...form.getInputProps("view_type")}
      />
      <Flex direction="column">
        <Text>Room Capacity</Text>

        <SegmentedControl
          size="xs"
          data={[
            { label: "1", value: "1" },
            { label: "2", value: "2" },
            { label: "3", value: "3" },
            { label: "4", value: "4" },
            { label: "5", value: "5" },
            { label: "6", value: "6" },
            { label: "7", value: "7" },
            { label: "8+", value: "8" },
          ]}
          {...form.getInputProps("room_capacity")}
        />
      </Flex>
      <Radio.Group
        name="Is Extendable"
        label="Is Extendable"
        {...form.getInputProps("is_extendable")}
      >
        <Group mt="xs">
          <Radio value="yes" label="Yes" />
          <Radio value="no" label="No" />
        </Group>
      </Radio.Group>
      <Textarea
        placeholder="Problems"
        label="Problems"
        {...form.getInputProps("room_problems")}
      />

      <Button
        type="submit"
        onClick={form.onSubmit(props.onSubmit as any) as any}
      >
        Submit
      </Button>
    </Stack>
  );
}
