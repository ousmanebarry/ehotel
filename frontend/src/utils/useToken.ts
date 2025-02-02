import jwt from "jwt-simple";
import Cookies from "js-cookie";
import { useLocalStorage } from "@mantine/hooks";
import { useState, useEffect } from "react";
import { Token } from "~/types";

export default function useToken() {
  const [token, setToken] = useState<Token>({
    user_ssn_sin: "",
    first_name: "",
    last_name: "",
    role: "customer",
  });
  const [firstName] = useLocalStorage({ key: "firstName", defaultValue: "" });
  const [lastName] = useLocalStorage({ key: "lastName", defaultValue: "" });

  useEffect(() => {
    const accessToken = Cookies.get("access_token") as string;
    if (accessToken) {
      let decodedToken = jwt.decode(accessToken, "", true);

      if (firstName) decodedToken.first_name = firstName;
      if (lastName) decodedToken.last_name = lastName;

      setToken(decodedToken);
    }
  }, [firstName, lastName]);

  return token;
}
