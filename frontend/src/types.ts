export interface Token {
  user_ssn_sin: string;
  first_name: string;
  last_name: string;
  role: string;
}

export interface RoomInfo {
  room_number: number;
  hotel_id: number;
  hotel_ID: number;
  room_capacity: number;
  view_type: string;
  price_per_night: number;
  is_extendable: boolean;
  room_problems: string;
}

export interface BookingInfo {
  booking_ID: number;
  booking_date: string;
  scheduled_check_in_date: string;
  scheduled_check_out_date: string;
  canceled: boolean;
  customer_SSN_SIN: number;
  room_number: number;
  hotel_ID: number;
}

export interface HotelChainInfo {
  chain_ID: number;
  name: string;
  number_of_hotels: number;
}

export interface HotelInfo {
  hotel_id: number;
  hotel_ID: number;
  chain_id: number;
  number_of_rooms: number;
  address_street_name: string;
  address_street_number: string;
  address_city: string;
  address_province_state: string;
  address_country: string;
  contact_email: string;
  star_rating: number;
}

export interface RentingInfo {
  rental_ID: number;
  base_price: number;
  date_paid: string;
  total_paid: number;
  discount: number;
  additional_charges: number;
  check_in_date: string;
  check_out_date: string;
  customer_SSN_SIN: number;
  booking_ID: number;
  room_number: number;
  hotel_ID: number;
  employee_ID: number;
  employee_SSN_SIN: number;
}

export interface RentingFormInfo {
  room_number: number;
  hotel_ID: number;
  customer_SSN_SIN: number;
  check_in_date: string;
  check_out_date: string;
  discount: number;
  additional_charges: number;
}

export interface HotelWithRooms extends HotelInfo {
  rooms: RoomInfo[];
}

export interface HotelChainSearch extends HotelChainInfo {
  hotels: HotelWithRooms[];
}
