import { URL } from "url";
import axios from "axios";
import { GetServerSideProps } from "next";
import Link from "next/link";
import { Center, Container, Table } from "@mantine/core";
import Header from "~/components/Header";

interface CapacityInfo {
  hotel_chain_name: string;
  chain_id: number;
  hotel_id: number;
  room_number: number;
  room_capacity: number;
}

interface HotelsProps {
  capacitiesInfo: CapacityInfo[];
  hotel_id?: number;
}

export default function Hotels(props: HotelsProps) {
  console.log(props.capacitiesInfo);
  return (
    <>
      <Header />
      <main>
        <Container size="sm">
          <Center sx={{ marginTop: "20px", marginBottom: "20px" }}>
            <Table>
              <thead>
                <tr>
                  <th>Chain Hotel</th>
                  <th>Hotel</th>
                  <th>Room Number</th>
                  <th>Capacity</th>
                </tr>
              </thead>
              <tbody>
                {props.capacitiesInfo
                  .filter((capacityInfo) =>
                    props.hotel_id
                      ? capacityInfo.hotel_id === props.hotel_id
                      : true
                  )
                  .map((capacityInfo) => (
                    <tr
                      key={`${capacityInfo.hotel_chain_name}-${capacityInfo.hotel_id}-${capacityInfo.room_number}`}
                    >
                      <td>{capacityInfo.hotel_chain_name}</td>
                      <td>
                        <Link
                          href={`/hotels?hotel_id=${capacityInfo.hotel_id}`}
                        >
                          {capacityInfo.hotel_id}
                        </Link>
                      </td>
                      <td>{capacityInfo.room_number}</td>
                      <td>{capacityInfo.room_capacity}</td>
                    </tr>
                  ))}
              </tbody>
            </Table>
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

  if ("hotel_id" in context.query) {
    const { data } = await axios.get<CapacityInfo[]>(
      `${process.env.NEXT_PUBLIC_URL}/hotel/hotel/total_capacity/${context.query.hotel_id}`
    );

    return {
      props: {
        capacitiesInfo: data,
        hotel_id: parseInt(context.query.hotel_id as string),
      },
    };
  } else {
    const { data } = await axios.get<CapacityInfo[]>(
      `${process.env.NEXT_PUBLIC_URL}/hotel/hotel/total_capacity`
    );

    return {
      props: { capacitiesInfo: data },
    };
  }
};
