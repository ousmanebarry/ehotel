import axios from "axios";
import jwt from "jwt-simple";
import Cookies from "js-cookie";
import { useRouter } from "next/router";
import Link from "next/link";
import { useForm, isNotEmpty, hasLength } from "@mantine/form";
import { message } from "antd";
import {
  TextInput,
  PasswordInput,
  Button,
  Text,
  Stack,
  Flex,
  Group,
  NumberInput,
  Radio,
} from "@mantine/core";
import { Token } from "~/types";

export default function SignUp() {
  const router = useRouter();

  const form = useForm({
    initialValues: {
      ssn: null,
      firstName: "",
      lastName: "",
      password: "",
      city: "",
      streetName: "",
      streetNumber: null,
      employeeId: null,
      hotelId: null,
      country: "",
      region: "",
      role: "",
      isManager: "no",
    },
    validate: {
      ssn: isNotEmpty("Enter your ssn"),
      firstName: isNotEmpty("Enter your first name"),
      lastName: isNotEmpty("Enter your last name"),
      streetName: isNotEmpty("Enter your street name"),
      streetNumber: isNotEmpty("Enter your street number"),
      city: isNotEmpty("Enter your city"),
      country: isNotEmpty("Enter your country"),
      region: isNotEmpty("Enter your region"),
      employeeId: isNotEmpty("Enter your employee id"),
      hotelId: isNotEmpty("Enter your hotelId"),
      role: isNotEmpty("Enter your role"),
      password: hasLength({ min: 6 }, "Password must be at least 6 characters"),
    },
    transformValues(values) {
      return {
        ...values,
        isManager: values.isManager === "yes",
      };
    },
  });

  const handleSubmit = form.onSubmit(async (info) => {
    try {
      await axios.post(`${process.env.NEXT_PUBLIC_URL}/auth/employees`, {
        employee_SSN_SIN: info.ssn,
        first_name: info.firstName,
        last_name: info.lastName,
        address_street_name: info.streetName,
        address_street_number: info.streetNumber,
        address_city: info.city,
        address_province_state: info.region,
        address_country: info.country,
        password: info.password,
        role: info.role,
        is_manager: info.isManager,
        hotel_ID: info.hotelId,
        employee_ID: info.employeeId,
      });

      const nextRes = await axios.post(
        `${process.env.NEXT_PUBLIC_URL}/auth/login`,
        {
          user_SSN_SIN: info.ssn,
          password: info.password,
          role: "employee",
        }
      );

      const access_token = nextRes.data["access_token"];
      const token: Token = jwt.decode(access_token, "", true);

      Cookies.set("access_token", nextRes.data["access_token"]);
      Cookies.set("role", token.role);
      router.push("/");
    } catch (error: any) {
      message.error(error.response.data.message);
    }
  });

  return (
    <Flex
      sx={{ height: "100%", marginTop: "20px" }}
      justify="center"
      align="center"
    >
      <Stack spacing="md" sx={{ padding: "40px" }}>
        <NumberInput
          placeholder="SSN"
          label="SSN"
          {...form.getInputProps("ssn")}
        />

        <Group position="apart">
          <NumberInput
            placeholder="Hotel ID"
            label="Hotel ID"
            {...form.getInputProps("hotelId")}
          />
          <NumberInput
            placeholder="Employee ID"
            label="Employee ID"
            {...form.getInputProps("employeeId")}
          />
        </Group>
        <Group position="apart">
          <TextInput
            placeholder="Role"
            label="Role"
            {...form.getInputProps("role")}
          />
          <Radio.Group
            name="Is Manager"
            label="Is Manager"
            {...form.getInputProps("isManager")}
          >
            <Group mt="xs">
              <Radio value="yes" label="Yes" />
              <Radio value="no" label="No" />
            </Group>
          </Radio.Group>
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
          <NumberInput
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
        <PasswordInput
          placeholder="Password"
          label="Password"
          {...form.getInputProps("password")}
        />
      </Stack>
      <Stack spacing="md">
        <Text>
          Already have an account{" "}
          <Link href="/login" style={{ textDecoration: "unset" }}>
            login
          </Link>
          .
        </Text>

        <Button type="submit" onClick={handleSubmit as any}>
          Sign Up
        </Button>
      </Stack>
    </Flex>
  );
}
