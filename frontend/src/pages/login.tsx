import axios from "axios";
import jwt from "jwt-simple";
import Cookies from "js-cookie";
import { GetServerSideProps } from "next";
import { useRouter } from "next/router";
import Link from "next/link";
import { useForm, isNotEmpty, hasLength } from "@mantine/form";
import { message } from "antd";
import {
  PasswordInput,
  Button,
  Text,
  Stack,
  Select,
  Center,
  NumberInput,
} from "@mantine/core";
import { Token } from "~/types";

export default function Login() {
  const router = useRouter();

  const form = useForm({
    initialValues: {
      ssn: 0,
      password: "",
      role: "",
    },
    validate: {
      ssn: isNotEmpty("Enter your ssn"),
      password: hasLength({ min: 6 }, "Password must be at least 6 characters"),
      role: isNotEmpty("Pick role"),
    },
  });

  const handleSubmit = form.onSubmit(async ({ ssn, password, role }) => {
    try {
      const res = await axios.post(
        `${process.env.NEXT_PUBLIC_URL}/auth/login`,
        {
          user_SSN_SIN: ssn,
          password,
          role,
        }
      );

      const access_token = res.data["access_token"];
      const token: Token = jwt.decode(access_token, "", true);

      Cookies.set("access_token", res.data["access_token"]);
      Cookies.set("role", token.role);
      router.push(role === "customer" ? "/" : "/employee");
    } catch (error: any) {
      message.error(error.response.data.message);
    }
  });

  return (
    <Center sx={{ height: "100%" }}>
      <Stack spacing="md">
        <NumberInput
          placeholder="SSN"
          label="SSN"
          {...form.getInputProps("ssn")}
        />
        <PasswordInput
          placeholder="Password"
          label="Password"
          {...form.getInputProps("password")}
        />
        <Select
          label="User Role"
          placeholder="User Role"
          data={[
            { value: "customer", label: "Customer" },
            { value: "employee", label: "Employee" },
          ]}
          {...form.getInputProps("role")}
        />

        <Text>
          Don&apos;t have an account{" "}
          <Link href="/signup" style={{ textDecoration: "unset" }}>
            signup
          </Link>
          .
        </Text>

        <Button type="submit" onClick={handleSubmit as any}>
          Login
        </Button>
      </Stack>
    </Center>
  );
}

export const getServerSideProps: GetServerSideProps<{}> = async (context) => {
  const access_token = context.req.cookies["access_token"];

  if (access_token) {
    const token: Token = jwt.decode(access_token, "", true);

    return {
      redirect: {
        destination: token.role === "customer" ? "/" : "/employee",
        permanent: false,
      },
    };
  }

  return {
    props: {},
  };
};
