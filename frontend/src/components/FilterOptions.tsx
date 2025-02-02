import { useEffect } from 'react';
import { useToggle } from '@mantine/hooks';
import { useForm } from '@mantine/form';
import {
	Box,
	Flex,
	Center,
	Modal,
	Button,
	Title,
	Text,
	Divider,
	Rating,
	SegmentedControl,
	Radio,
	NumberInput,
} from '@mantine/core';
import { IconAdjustments } from '@tabler/icons';
import useSearchQuery from '~/utils/useSearchQuery';
import useHotelChains from '~/utils/useHotelChains';

export default function FilterOptions() {
	const [open, toggle] = useToggle();
	const [setSearchQuery] = useSearchQuery((state) => [state.setQuery, state.setDateRange]);

	const form = useForm({
		initialValues: {
			price: null,
			hotelChain: '',
			category: 0,
			roomCapacity: 'any',
		},
	});

	const hotelChains = useHotelChains((state) => state.hotelChains);

	useEffect(() => {
		setSearchQuery(form.values);
	}, [form.values]);

	return (
		<>
			<Button
				onClick={() => toggle()}
				leftIcon={<IconAdjustments />}
				variant='outline'
				color='dark'
				sx={{
					borderColor: 'rgb(206, 212, 218)',
					':hover': { backgroundColor: 'unset' },
				}}
			>
				Filter
			</Button>
			<Modal
				opened={open}
				onClose={() => toggle()}
				size='800px'
				transition='scale'
				overflow='inside'
				centered
				title={
					<Center>
						<Title order={4}>Filters</Title>
					</Center>
				}
			>
				<Box sx={{ padding: '0px 20px' }}>
					<Flex rowGap='20px' direction='column' sx={{ margin: '20px' }}>
						<Title order={3} sx={{ marginBottom: '-20px' }}>
							Max Price
						</Title>
						<NumberInput icon='$' {...form.getInputProps('price')} />
					</Flex>

					<Divider />

					<Flex rowGap='20px' direction='column' sx={{ margin: '20px' }}>
						<Title order={3}>Hotel</Title>

						{hotelChains.length > 0 && (
							<Flex direction='column' rowGap='8px'>
								<Text>Hotel Chain</Text>
								<Radio.Group {...form.getInputProps('hotelChain')}>
									{hotelChains.map((chain) => (
										<Radio
											key={chain.chain_ID}
											value={chain.name}
											label={chain.name}
											onClick={() => {
												if (form.values.hotelChain === chain.name) {
													form.setValues({ hotelChain: '' });
												}
											}}
										/>
									))}
								</Radio.Group>
							</Flex>
						)}

						<Flex direction='column' rowGap='8px'>
							<Text>Category</Text>
							<Rating size='lg' {...form.getInputProps('category')} />
						</Flex>
					</Flex>

					<Divider />

					<Flex rowGap='20px' direction='column' sx={{ margin: '20px' }}>
						<Title order={3}>Room Capacity</Title>

						<SegmentedControl
							data={[
								{ label: 'Any', value: 'any' },
								{ label: '1', value: '1' },
								{ label: '2', value: '2' },
								{ label: '3', value: '3' },
								{ label: '4', value: '4' },
								{ label: '5', value: '5' },
								{ label: '6', value: '6' },
								{ label: '7', value: '7' },
								{ label: '8+', value: '8' },
							]}
							{...form.getInputProps('roomCapacity')}
						/>
					</Flex>
				</Box>
			</Modal>
		</>
	);
}
