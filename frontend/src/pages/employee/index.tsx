import axios from "axios";
import dayjs from "dayjs";
import { useEffect, useRef, useState } from "react";
import { Container, Text, Flex, Center, Loader } from "@mantine/core";
import Room from "~/components/Room";
import Header from "~/components/Header";
import useSearchQuery from "~/utils/useSearchQuery";
import { RoomInfo, HotelInfo, HotelChainInfo } from "~/types";

type RoomQuery = { room: RoomInfo; hotel: HotelInfo };

export default function Home() {
  const {
    startDate,
    endDate,
    price,
    hotelChain,
    category,
    roomCapacity,
    location,
  } = useSearchQuery((state) => state);
  const debounceState = useRef<null | number>(null);
  const [result, setResult] = useState<RoomQuery[]>([]);
  const [loading, setLoading] = useState(true);
  const firstRender = useRef(true);
  const [hotelChains, setHotelChains] = useState<HotelChainInfo[]>([]);

  useEffect(() => {
    axios
      .get<HotelChainInfo[]>(
        `${process.env.NEXT_PUBLIC_URL}/hotel_chain/hotel_chain`
      )
      .then((res) => {
        const { data } = res;

        setHotelChains(data);
      });
  }, []);

  useEffect(() => {
    if (debounceState.current != null) {
      clearTimeout(debounceState.current as number);
    }

    debounceState.current = setTimeout(() => {
      setLoading(true);

      axios
        .get<RoomQuery[]>(`${process.env.NEXT_PUBLIC_URL}/room/room`)
        .then((res) => {
          firstRender.current = false;
          setLoading(false);
          setResult(res.data);
        });

      debounceState.current = null;
    }, 1000) as any;
  }, [startDate, endDate, price, hotelChain, category, roomCapacity, location]);

  return (
    <>
      <Header />
      <main>
        <Container sx={{ marginTop: "20px", marginBottom: "20px" }}>
          <Center>
            <Flex wrap="wrap" gap="30px">
              {result.map((room) => (
                <Room
                  key={`${room.room.room_number}-${room.hotel.hotel_ID}-${room.hotel.chain_id}`}
                  room={room.room}
                  hotel={room.hotel}
                  hotelChains={hotelChains}
                />
              ))}
              {result.length === 0 && !loading && (
                <Text>No rooms available with the given criteria</Text>
              )}
              {firstRender.current && <Loader />}
            </Flex>
          </Center>
        </Container>
      </main>
    </>
  );
}
