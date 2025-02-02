import axios from "axios";
import { GetServerSideProps } from "next";
import { Center, Text, Container, Flex } from "@mantine/core";
import Header from "~/components/Header";
import Hotel from "~/components/Hotel";
import { HotelInfo } from "~/types";

interface HotelsProps {
  hotels: HotelInfo[];
}

export default function Hotels(props: HotelsProps) {
  return (
    <>
      <Header />
      <main>
        <Container sx={{ marginTop: "20px", marginBottom: "20px" }}>
          <Center>
            <Flex wrap="wrap" gap="30px">
              {props.hotels.map((hotel) => (
                <Hotel hotel={hotel} key={hotel.hotel_id} />
              ))}
              {props.hotels.length === 0 && (
                <Text>There currently aren't any hotels</Text>
              )}
            </Flex>
          </Center>
        </Container>
      </main>
    </>
  );
}

export const getServerSideProps: GetServerSideProps<HotelsProps> = async (
  context
) => {
  const access_token = context.req.cookies["access_token"];

  if (!access_token) {
    return {
      redirect: { destination: "/login", permanent: false },
    };
  }

  const { data } = await axios.get<HotelInfo[]>(
    `${process.env.NEXT_PUBLIC_URL}/hotel/hotel`
  );

  return {
    props: { hotels: data },
  };
};
