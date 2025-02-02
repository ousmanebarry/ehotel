import { useEffect } from "react";
import { useForm, isNotEmpty, isEmail } from "@mantine/form";
import {
  TextInput,
  Button,
  Stack,
  Group,
  NumberInput,
  Rating,
  Text,
} from "@mantine/core";
import { HotelInfo } from "~/types";

interface HotelForm {
  hotel?: HotelInfo;
  setFormReset?: (formReset: () => void) => void;
  onSubmit: (hotel: HotelInfo) => void;
}

export default function HotelForm(props: HotelForm) {
  const form = useForm({
    initialValues: {
      chain_id: props.hotel?.chain_id,
      hotel_id: props.hotel?.hotel_id,
      number_of_rooms: props.hotel?.number_of_rooms,
      address_street_name: props.hotel?.address_street_name,
      address_street_number: props.hotel?.address_street_number,
      address_city: props.hotel?.address_city,
      address_country: props.hotel?.address_country,
      address_province_state: props.hotel?.address_province_state,
      contact_email: props.hotel?.contact_email,
      star_rating: props.hotel?.star_rating,
    },
    validate: {
      chain_id: isNotEmpty("Enter chain Id"),
      hotel_id: isNotEmpty("Enter hotel Id"),
      number_of_rooms: isNotEmpty("Enter number of rooms"),
      address_street_name: isNotEmpty("Enter street name"),
      address_street_number: isNotEmpty("Enter street number"),
      address_city: isNotEmpty("Enter city"),
      address_country: isNotEmpty("Enter country"),
      address_province_state: isNotEmpty("Enter region"),
      contact_email: isEmail("Enter valid contact email"),
      star_rating: isNotEmpty("Enter start rating"),
    },
  });

  useEffect(() => {
    if (props.setFormReset)
      props.setFormReset(() => () => {
        form.setValues({
          contact_email: "",
          address_city: "",
          address_country: "",
          address_province_state: "",
          address_street_name: "",
          address_street_number: "",
          star_rating: undefined,
          chain_id: undefined,
          hotel_id: undefined,
          number_of_rooms: undefined,
        });
      });
  }, [form.reset, props.setFormReset]);

  return (
    <Stack spacing="md" sx={{ padding: "20px" }}>
      {!props.hotel && (
        <Group align="center">
          <NumberInput
            placeholder="Hotel Id"
            label="Hotel Id"
            {...form.getInputProps("hotel_id")}
          />
          <NumberInput
            placeholder="Chain Id"
            label="Chain Id"
            {...form.getInputProps("chain_id")}
          />
        </Group>
      )}
      <NumberInput
        placeholder="Number of Rooms"
        label="Number of Rooms"
        {...form.getInputProps("number_of_rooms")}
      />
      <Group align="center">
        <TextInput
          placeholder="Street Name"
          label="Street Name"
          {...form.getInputProps("address_street_name")}
        />
        <NumberInput
          placeholder="Street Number"
          label="Street Number"
          {...form.getInputProps("address_street_number")}
        />
      </Group>
      <TextInput
        placeholder="City"
        label="City"
        {...form.getInputProps("address_city")}
      />
      <Group align="center">
        <TextInput
          placeholder="Country"
          label="Country"
          {...form.getInputProps("address_country")}
        />
        <TextInput
          placeholder="Region"
          label="Region"
          {...form.getInputProps("address_province_state")}
        />
      </Group>
      <TextInput
        icon="@"
        placeholder="Contact Email"
        label="Contact Email"
        {...form.getInputProps("contact_email")}
      />
      <Stack>
        <Text>Star Rating</Text>
        <Rating {...form.getInputProps("star_rating")} />
        <Text size="xs" sx={{ marginTop: "-10px" }} color="red">
          {form.errors.star_rating}
        </Text>
      </Stack>

      <Button
        type="submit"
        onClick={form.onSubmit(props.onSubmit as any) as any}
      >
        Submit
      </Button>
    </Stack>
  );
}
