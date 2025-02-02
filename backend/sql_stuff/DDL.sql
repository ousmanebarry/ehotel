DROP TABLE IF EXISTS Rental;
DROP TABLE IF EXISTS Booking;
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Room;
DROP TABLE IF EXISTS Hotel_Phone_Number;
DROP TABLE IF EXISTS Hotel_Chain_Phone_Number;
DROP TABLE IF EXISTS Hotel_Chain_Contact_Email;
DROP TABLE IF EXISTS Hotel_Chain_Central_Office_Address;
DROP TABLE IF EXISTS Employee_Role;
DROP TABLE IF EXISTS Employee;
DROP TABLE IF EXISTS Hotel;
DROP TABLE IF EXISTS Hotel_Chain;
DROP TABLE IF EXISTS Has_Amenity;
DROP TABLE IF EXISTS Amenity;

CREATE TABLE Hotel_Chain (
  chain_ID INT,
  name VARCHAR(50) NOT NULL,
  number_of_hotels INT NOT NULL,
  PRIMARY KEY (chain_ID)
);

CREATE TABLE Hotel (
  hotel_ID INT,
  chain_ID INT,
  number_of_rooms INT,
  address_street_name VARCHAR(50) NOT NULL,
  address_street_number INT NOT NULL,
  address_city VARCHAR(50) NOT NULL,
  address_province_state VARCHAR(50) NOT NULL,
  address_country VARCHAR(50) NOT NULL,
  contact_email VARCHAR(50) NOT NULL,
  star_rating INT NOT NULL,
  PRIMARY KEY (hotel_ID),
  FOREIGN KEY (chain_ID) REFERENCES Hotel_Chain(chain_ID) ON DELETE CASCADE,
  CONSTRAINT uc_address UNIQUE (address_street_name, address_street_number, address_city, address_province_state, address_country)
);

CREATE TABLE Employee (
  employee_SSN_SIN INT,
  employee_ID INT,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  address_street_name VARCHAR(50) NOT NULL,
  address_street_number INT NOT NULL,
  address_city VARCHAR(50) NOT NULL,
  address_province_state VARCHAR(50) NOT NULL,
  address_country VARCHAR(50) NOT NULL,
  hotel_ID INT NOT NULL,
  is_manager BOOLEAN NOT NULL,
  PRIMARY KEY (employee_SSN_SIN, employee_ID),
  FOREIGN KEY (hotel_ID) REFERENCES Hotel(hotel_ID) ON DELETE SET NULL
);

CREATE TABLE Employee_Role (
  employee_SSN_SIN INT,
  employee_ID INT,
  role VARCHAR(50) NOT NULL,
  PRIMARY KEY (employee_SSN_SIN, employee_ID, role),
  FOREIGN KEY (employee_SSN_SIN, employee_ID) REFERENCES Employee(employee_SSN_SIN, employee_ID) ON DELETE CASCADE
);

CREATE TABLE Hotel_Phone_Number (
  hotel_ID INT,
  phone_number VARCHAR(20),
  PRIMARY KEY (hotel_ID, phone_number),
  FOREIGN KEY (hotel_ID) REFERENCES Hotel(hotel_ID) ON DELETE CASCADE
);

CREATE TABLE Hotel_Chain_Central_Office_Address (
  chain_ID INT,
  address_street_name VARCHAR(50) NOT NULL,
  address_street_number INT NOT NULL,
  address_city VARCHAR(50) NOT NULL,
  address_province_state VARCHAR(50) NOT NULL,
  address_country VARCHAR(50) NOT NULL,
  PRIMARY KEY (chain_ID),
  FOREIGN KEY (chain_ID) REFERENCES Hotel_Chain(chain_ID) ON DELETE CASCADE
);

CREATE TABLE Hotel_Chain_Contact_Email (
  chain_ID INT,
  contact_email VARCHAR(50) NOT NULL,
  PRIMARY KEY (chain_ID),
  FOREIGN KEY (chain_ID) REFERENCES Hotel_Chain(chain_ID) ON DELETE CASCADE
);

CREATE TABLE Hotel_Chain_Phone_Number (
  chain_ID INT,
  phone_number VARCHAR(12),
  PRIMARY KEY (chain_ID, phone_number),
  FOREIGN KEY (chain_ID) REFERENCES Hotel_Chain(chain_ID) ON DELETE CASCADE
);

CREATE TABLE Room (
  room_number INT,
  hotel_ID INT,
  room_capacity INT NOT NULL,
  view_type VARCHAR(50) NOT NULL,
  price_per_night INT NOT NULL,
  is_extendable BOOLEAN NOT NULL,
  room_problems TEXT,
  PRIMARY KEY (room_number, hotel_ID),
  FOREIGN KEY (hotel_ID) REFERENCES Hotel(hotel_ID) ON DELETE CASCADE
);

CREATE TABLE Amenity (
  amenity_id INT,
  amenity_name VARCHAR(50) NOT NULL,
  PRIMARY KEY (amenity_id) 
);

CREATE TABLE Has_Amenity (
  amenity_id INT,
  hotel_id INT,
  room_number INT,
  PRIMARY KEY (amenity_id, hotel_id, room_number),
  FOREIGN KEY (hotel_id, room_number) REFERENCES Room(hotel_ID, room_number) ON DELETE CASCADE
);

CREATE TABLE Customer (
    customer_SSN_SIN INT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    address_street_name VARCHAR(50) NOT NULL,
    address_street_number INT NOT NULL,
    address_city VARCHAR(50) NOT NULL,
    address_province_state VARCHAR(50) NOT NULL,
    address_country VARCHAR(50) NOT NULL,
    registration_date DATE NOT NULL,
    PRIMARY KEY (customer_SSN_SIN)
);

CREATE TABLE Booking (
    booking_ID SERIAL,
    booking_date DATE NOT NULL,
    scheduled_check_in_date DATE NOT NULL,
    scheduled_check_out_date DATE NOT NULL,
    canceled BOOLEAN NOT NULL DEFAULT false,
    customer_SSN_SIN INT,
    room_number INT,
    hotel_ID INT,
    PRIMARY KEY (booking_ID),
    FOREIGN KEY (customer_SSN_SIN) REFERENCES Customer(customer_SSN_SIN) ON DELETE CASCADE,
    FOREIGN KEY (room_number, hotel_ID) REFERENCES Room(room_number, hotel_ID) ON DELETE SET NULL
);

CREATE TABLE Rental (
  rental_ID SERIAL,
  base_price INT NOT NULL,
  date_paid DATE NOT NULL,
  total_paid INT NOT NULL,
  discount INT NOT NULL,
  additional_charges INT NOT NULL,
  check_in_date DATE NOT NULL,
  check_out_date DATE NOT NULL,
  customer_SSN_SIN INT,
  booking_ID INT,
  room_number INT,
  hotel_ID INT,
  employee_ID INT,
  employee_SSN_SIN INT,
  PRIMARY KEY (rental_ID),
  FOREIGN KEY (customer_SSN_SIN) REFERENCES Customer(customer_SSN_SIN) ON DELETE CASCADE,
  FOREIGN KEY (employee_SSN_SIN, employee_ID) REFERENCES Employee(employee_SSN_SIN, employee_ID),
  FOREIGN KEY (booking_ID) REFERENCES Booking(booking_ID),
  FOREIGN KEY (room_number, hotel_ID) REFERENCES Room(room_number, hotel_ID) ON DELETE SET NULL
);

CREATE TABLE Users (
    user_SSN_SIN INT PRIMARY KEY,
    password VARCHAR(1024) NOT NULL,
    role VARCHAR(10) NOT NULL,
    CHECK (role = 'customer' OR role = 'employee')
);

--Index creation 
create index hotel_ID on hotel(hotel_id);

create index room_number on room(room_number);

create index chain_id on hotel_chain(chain_id);

create index customer_ssn_sin on customer(customer_ssn_sin);

create index employee_ssn_sin on employee(employee_ssn_sin);

--Triggers for incrementing hotels on insert, decrementing number of hotels on delete
create or replace function incr_number_of_hotels()
returns trigger as
    $$
begin
    update hotel_chain
    set number_of_hotels = number_of_hotels + 1
    where chain_id = new.chain_id;
    return new;
end;
$$ 
    language plpgsql;

create trigger incr_hotel_trigger
after insert on hotel
for each row
execute function incr_number_of_hotels();

create or replace function decr_number_of_hotels()
returns trigger as
    $$
begin
    update hotel_chain
    set number_of_hotels = number_of_hotels - 1
    where chain_id = old.chain_id;
    return old;
end;
$$ 
    language plpgsql;

create trigger decr_hotel_trigger
after delete on hotel
for each row
execute function decr_number_of_hotels();


--triggers for incrementing number of rooms in hotel on insert, decrementing number of rooms in hotel on delete
create or replace function incr_number_of_rooms()
returns trigger as 
    $$
begin
  update hotel
  set number_of_rooms = number_of_rooms + 1
  where hotel_id = new.hotel_id;
  return new;
end;
$$ 
    language plpgsql;

create trigger incr_room_trigger
after insert on room
for each row
execute function incr_number_of_rooms();

create or replace function decr_number_of_rooms()
returns trigger as
    $$
begin
  update hotel
  set number_of_rooms = number_of_rooms - 1
  where hotel_id = old.hotel_id;
  return old;
end;
$$ 
    language plpgsql;

create trigger decr_room_trigger
after delete on room
for each row
execute function decr_number_of_rooms();
