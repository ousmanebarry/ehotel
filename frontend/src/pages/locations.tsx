import axios from "axios";
import dayjs from "dayjs";
import { GetServerSideProps } from "next";
import { Center, Container, Table, Text } from "@mantine/core";
import Header from "~/components/Header";

interface LocationInfo {
  country: string;
  state_province: string;
  city: string;
  available_rooms: number;
}

interface LocationProps {
  locationsInfo: LocationInfo[];
}

export default function Location(props: LocationProps) {
  return (
    <>
      <Header />
      <main>
        <Container size="xs">
          <Center sx={{ marginTop: "20px", marginBottom: "20px" }}>
            {props.locationsInfo.length > 0 && (
              <Table>
                <thead>
                  <tr>
                    <th>Location</th>
                    <th>Available Rooms</th>
                  </tr>
                </thead>
                <tbody>
                  {props.locationsInfo.map((locationInfo) => (
                    <tr
                      key={`${locationInfo.city} - ${locationInfo.state_province}, ${locationInfo.country}`}
                    >
                      <td>{`${locationInfo.city} - ${locationInfo.state_province}, ${locationInfo.country}`}</td>
                      <td>{locationInfo.available_rooms}</td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            )}
            {props.locationsInfo.length === 0 && (
              <Text>No rooms currently available</Text>
            )}
          </Center>
        </Container>
      </main>
    </>
  );
}

export const getServerSideProps: GetServerSideProps<LocationProps> = async (
  context
) => {
  const access_token = context.req.cookies["access_token"];

  if (!access_token) {
    return {
      redirect: { destination: "/login", permanent: false },
    };
  }

  const { data } = await axios.get<LocationInfo[]>(
    `${process.env.NEXT_PUBLIC_URL}/room/available-rooms`,
    {
      params: {
        start_date: dayjs().subtract(10, "years").format("YYYY-MM-DD"),
        end_date: dayjs().add(10, "years").format("YYYY-MM-DD"),
      },
      headers: { Authorization: `Bearer ${access_token}` },
    }
  );

  return {
    props: { locationsInfo: data },
  };
};
