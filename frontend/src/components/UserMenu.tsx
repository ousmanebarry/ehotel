import Cookies from "js-cookie";
import { useRouter } from "next/router";
import Link from "next/link";
import { useLocalStorage } from "@mantine/hooks";
import { Text, Menu, UnstyledButton, Center } from "@mantine/core";
import {
  IconUserCircle,
  IconUser,
  IconBook,
  IconLogout,
  IconPlus,
  IconBuilding,
  IconMap
} from "@tabler/icons";
import useToken from "~/utils/useToken";

export default function UserMenu() {
  const setFirstName = useLocalStorage({
    key: "firstName",
    defaultValue: "",
  })[1];
  const setLastName = useLocalStorage({ key: "lastName", defaultValue: "" })[1];

  const router = useRouter();
  const token = useToken();

  const handleLogout = () => {
    setFirstName("");
    setLastName("");
    Cookies.remove("access_token");
    router.push("/login");
  };

  return (
    <Menu shadow="md">
      <Menu.Target>
        <UnstyledButton>
          <Center inline>
            <IconUserCircle />
            <Text size="sm" sx={{ paddingLeft: "8px" }}>
              {`${token.first_name} ${token.last_name}`}
            </Text>
          </Center>
        </UnstyledButton>
      </Menu.Target>
      {token.role === "customer" && (
        <Menu.Dropdown>
          <Link href="/account" style={{ textDecoration: "unset" }}>
            <Menu.Item icon={<IconUser size={14} />}>Account</Menu.Item>
          </Link>
          <Link href="/bookings" style={{ textDecoration: "unset" }}>
            <Menu.Item icon={<IconBook size={14} />}>Bookings</Menu.Item>
          </Link>
          <Link href="/rentings" style={{ textDecoration: "unset" }}>
            <Menu.Item icon={<IconBook size={14} />}>Rentings</Menu.Item>
          </Link>
          <Link href="/hotels" style={{ textDecoration: "unset" }}>
            <Menu.Item icon={<IconBuilding size={14} />}>Hotels</Menu.Item>
          </Link>
          <Link href="/locations" style={{ textDecoration: "unset" }}>
            <Menu.Item icon={<IconMap size={14} />}>Locations</Menu.Item>
          </Link>
          <Menu.Item icon={<IconLogout size={14} />} onClick={handleLogout}>
            Logout
          </Menu.Item>
        </Menu.Dropdown>
      )}
      {token.role === "employee" && (
        <Menu.Dropdown>
          <Link href="/employee/account" style={{ textDecoration: "unset" }}>
            <Menu.Item icon={<IconUser size={14} />}>Account</Menu.Item>
          </Link>
          <Link href="/employee/bookings" style={{ textDecoration: "unset" }}>
            <Menu.Item icon={<IconBook size={14} />}>Bookings</Menu.Item>
          </Link>
          <Link href="/employee/hotels" style={{ textDecoration: "unset" }}>
            <Menu.Item icon={<IconBuilding size={14} />}>Hotels</Menu.Item>
          </Link>
          <Link href="/employee/add-hotel" style={{ textDecoration: "unset" }}>
            <Menu.Item icon={<IconPlus size={14} />}>Add Hotel</Menu.Item>
          </Link>
          <Link href="/employee/add-room" style={{ textDecoration: "unset" }}>
            <Menu.Item icon={<IconPlus size={14} />}>Add Room</Menu.Item>
          </Link>
          <Link
            href="/employee/create-renting"
            style={{ textDecoration: "unset" }}
          >
            <Menu.Item icon={<IconPlus size={14} />}>Create Renting</Menu.Item>
          </Link>
          <Menu.Item icon={<IconLogout size={14} />} onClick={handleLogout}>
            Logout
          </Menu.Item>
        </Menu.Dropdown>
      )}
    </Menu>
  );
}
