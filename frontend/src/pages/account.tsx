import { GetServerSideProps } from "next";
import axios from "axios";
import Cookies from "js-cookie";
import jwt from "jwt-simple";
import { useLocalStorage } from "@mantine/hooks";
import { useForm, isNotEmpty } from "@mantine/form";
import { message } from "antd";
import { TextInput, Button, Stack, Center, Group } from "@mantine/core";
import Header from "~/components/Header";
import useToken from "~/utils/useToken";

interface UserInfo {
  firstName: string;
  lastName: string;
  city: string;
  streetName: string;
  streetNumber: string;
  country: string;
  region: string;
}

export default function Account(props: UserInfo) {
  const token = useToken();

  const [firstName, setFirstName] = useLocalStorage({
    key: "firstName",
    defaultValue: "",
  });
  const [lastName, setLastName] = useLocalStorage({
    key: "lastName",
    defaultValue: "",
  });

  const form = useForm({
    initialValues: {
      ...props,
    },
    validate: {
      firstName: isNotEmpty("Enter your first name"),
      lastName: isNotEmpty("Enter your last name"),
      streetName: isNotEmpty("Enter your street name"),
      streetNumber: isNotEmpty("Enter your street number"),
      city: isNotEmpty("Enter your city"),
      country: isNotEmpty("Enter your country"),
      region: isNotEmpty("Enter your region"),
    },
  });

  const handleSubmit = form.onSubmit(async (info) => {
    try {
      const res = await axios.put(
        `${process.env.NEXT_PUBLIC_URL}/auth/customers/${token.user_ssn_sin}`,
        {
          first_name: info.firstName,
          last_name: info.lastName,
          address_street_name: info.streetName,
          address_street_number: info.streetNumber,
          address_city: info.city,
          address_province_state: info.region,
          address_country: info.country,
        },
        {
          headers: { Authorization: `Bearer ${Cookies.get("access_token")}` },
        }
      );

      setFirstName(info.firstName);
      setLastName(info.lastName);
      message.success("Updated user info");
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
            <Group align="center">
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
            <Group align="center">
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
            <Group align="center">
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

            <Button type="submit" onClick={handleSubmit as any}>
              Update
            </Button>
          </Stack>
        </Center>
      </main>
    </>
  );
}

export const getServerSideProps: GetServerSideProps<UserInfo> = async (
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
    `${process.env.NEXT_PUBLIC_URL}/auth/customers/${token.user_ssn_sin}`,
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
    },
  };
};
