import axios from "axios";
import jwt from "jwt-simple";
import { GetServerSideProps } from "next";
import { Flex, Text, Center } from "@mantine/core";
import Header from "~/components/Header";
import Renting from "~/components/Renting";
import { RentingInfo, Token } from "~/types";

interface RentingsProps {
  rentings: RentingInfo[];
}

export default function Rentings(props: RentingsProps) {
  return (
    <>
      <Header />
      <main>
        <Center sx={{ marginTop: "20px", marginBottom: "20px" }}>
          <Flex wrap="wrap" gap="30px">
            {props.rentings.map((renting) => (
              <Renting renting={renting} key={renting.rental_ID} />
            ))}
            {props.rentings.length === 0 && (
              <Text>You do not currently have any rentings</Text>
            )}
          </Flex>
        </Center>
      </main>
    </>
  );
}

export const getServerSideProps: GetServerSideProps<RentingsProps> = async (
  context
) => {
  const access_token = context.req.cookies["access_token"];

  if (!access_token) {
    return {
      redirect: { destination: "/login", permanent: false },
    };
  }

  const token: Token = jwt.decode(access_token, "", true);

  const { data } = await axios.get<RentingInfo[]>(
    `${process.env.NEXT_PUBLIC_URL}/rental/rentals/${token.user_ssn_sin}`,
    {
      headers: { Authorization: `Bearer ${access_token}` },
    }
  );

  return {
    props: { rentings: data },
  };
};
