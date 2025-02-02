import { GetServerSideProps } from "next";
import axios from "axios";
import Cookies from "js-cookie";
import jwt from "jwt-simple";
import { useLocalStorage } from "@mantine/hooks";
import { useForm, isNotEmpty } from "@mantine/form";
import { message } from "antd";
import {
  TextInput,
  Button,
  Stack,
  Center,
  Group,
  NumberInput,
  Radio,
} from "@mantine/core";
import Header from "~/components/Header";
import useToken from "~/utils/useToken";

interface EmployeeInfo {
  firstName: string;
  lastName: string;
  city: string;
  streetName: string;
  streetNumber: string;
  country: string;
  region: string;
  employee_ID: number;
  hotel_ID: number;
  is_manager: boolean;
}

export default function Account(props: EmployeeInfo) {
  const token = useToken();

  const setFirstName = useLocalStorage({
    key: "firstName",
    defaultValue: "",
  })[1];
  const setLastName = useLocalStorage({
    key: "lastName",
    defaultValue: "",
  })[1];

  const form = useForm({
    initialValues: {
      ...props,
      is_manager: props.is_manager ? "yes" : "no",
    },
    validate: {
      firstName: isNotEmpty("Enter your first name"),
      lastName: isNotEmpty("Enter your last name"),
      streetName: isNotEmpty("Enter your street name"),
      streetNumber: isNotEmpty("Enter your street number"),
      city: isNotEmpty("Enter your city"),
      country: isNotEmpty("Enter your country"),
      region: isNotEmpty("Enter your region"),
      employee_ID: isNotEmpty("Enter your employee ID"),
      hotel_ID: isNotEmpty("Enter your hotel ID"),
    },
    transformValues(values) {
      return {
        ...values,
        is_manager: values.is_manager === "yes",
      };
    },
  });

  const handleSubmit = form.onSubmit(async (info) => {
    try {
      let promote_to_manager = null;
      let demote_from_manager = null;

      if (props.is_manager && !info.is_manager) {
        demote_from_manager = true;
      }
      if (!props.is_manager && info.is_manager) {
        promote_to_manager = true;
      }

      await axios.put(
        `${process.env.NEXT_PUBLIC_URL}/auth/employees/${token.user_ssn_sin}`,
        {
          first_name: info.firstName,
          last_name: info.lastName,
          address_street_name: info.streetName,
          address_street_number: info.streetNumber,
          address_city: info.city,
          address_province_state: info.region,
          address_country: info.country,
          hotel_ID: info.hotel_ID,
          employee_ID: info.employee_ID,
          promote_to_manager,
          demote_from_manager,
        },
        {
          headers: { Authorization: `Bearer ${Cookies.get("access_token")}` },
        }
      );

      setFirstName(info.firstName);
      setLastName(info.lastName);
      message.success("Updated employee info");
    } catch {
      message.error("Something went wrong while trying to update your account");
    }
  });

  return (
    <>
      <Header displayFilter={false} />
      <main>
        <Center sx={{ height: "100%", marginTop: "20px" }}>
          <Stack spacing="md">
            <Group position="apart">
              <NumberInput
                placeholder="Hotel ID"
                label="Hotel ID"
                {...form.getInputProps("hotel_ID")}
              />
              <TextInput
                placeholder="Employee ID"
                label="Employee ID"
                {...form.getInputProps("employee_ID")}
              />
            </Group>
            <Group position="apart">
              <TextInput
                placeholder="First Name"
                label="First Name"
                {...form.getInputProps("firstName")}
              />
              <TextInput
                placeholder="Last Name"
                label="Last Name"
                {...form.getInputProps("lastName")}
              />
            </Group>
            <Group position="apart">
              <TextInput
                placeholder="Street Name"
                label="Street Name"
                {...form.getInputProps("streetName")}
              />
              <TextInput
                placeholder="Street Number"
                label="Street Number"
                {...form.getInputProps("streetNumber")}
              />
            </Group>
            <TextInput
              placeholder="City"
              label="City"
              {...form.getInputProps("city")}
            />
            <Group position="apart">
              <TextInput
                placeholder="Country"
                label="Country"
                {...form.getInputProps("country")}
              />
              <TextInput
                placeholder="Region"
                label="Region"
                {...form.getInputProps("region")}
              />
            </Group>

            <Radio.Group
              name="Is Manager"
              label="Is Manager"
              {...form.getInputProps("is_manager")}
              sx={{ paddingBottom: "10px" }}
            >
              <Group mt="xs">
                <Radio value="yes" label="Yes" />
                <Radio value="no" label="No" />
              </Group>
            </Radio.Group>

            <Button type="submit" onClick={handleSubmit as any}>
              Update
            </Button>
          </Stack>
        </Center>
      </main>
    </>
  );
}

export const getServerSideProps: GetServerSideProps<EmployeeInfo> = async (
  context
) => {
  const access_token = context.req.cookies["access_token"];

  if (!access_token) {
    return {
      redirect: { destination: "/login", permanent: false },
    };
  }

  const token = jwt.decode(access_token, "", true);

  const { data } = await axios.get(
    `${process.env.NEXT_PUBLIC_URL}/auth/employees/${token.user_ssn_sin}`,
    {
      headers: { Authorization: `Bearer ${access_token}` },
    }
  );

  return {
    props: {
      firstName: data.first_name,
      lastName: data.last_name,
      city: data.address_city,
      streetName: data.address_street_name,
      streetNumber: data.address_street_number,
      country: data.address_country,
      region: data.address_province_state,
      employee_ID: data.employee_ID,
      hotel_ID: data.hotel_ID,
      is_manager: data.is_manager,
    },
  };
};
