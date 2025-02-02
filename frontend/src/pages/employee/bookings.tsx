import jwt from 'jwt-simple';
import axios from 'axios';
import { GetServerSideProps } from 'next';
import { Flex, Text, Center } from '@mantine/core';
import Header from '~/components/Header';
import Booking from '~/components/Booking';
import { BookingInfo, Token } from '~/types';

interface BookingsProps {
	bookings: BookingInfo[];
}

export default function Bookings(props: BookingsProps) {
	return (
		<>
			<Header />
			<main>
				<Center sx={{ marginTop: '20px', marginBottom: '20px' }}>
					<Flex wrap='wrap' gap='30px'>
						{props.bookings.length > 0 ? (
							props.bookings.map((booking) => <Booking booking={booking} key={booking.booking_ID} />)
						) : (
							<Text>There currently aren't any bookings</Text>
						)}
					</Flex>
				</Center>
			</main>
		</>
	);
}

export const getServerSideProps: GetServerSideProps<BookingsProps> = async (context) => {
	try {
		const access_token = context.req.cookies['access_token'];

		if (!access_token) {
			return {
				redirect: { destination: '/login', permanent: false },
			};
		}

		const { data } = await axios.get<BookingInfo[]>(`${process.env.NEXT_PUBLIC_URL}/booking/all_bookings`, {
			headers: { Authorization: `Bearer ${access_token}` },
		});
		console.log(data);
		return {
			props: { bookings: data },
		};
	} catch (error) {
		return {
			props: {
				bookings: [],
			},
		};
	}
};
