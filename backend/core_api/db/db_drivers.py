from sqlalchemy.sql.expression import text
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from random import randint
import os
import psycopg2
import datetime
import random
import traceback

load_dotenv()
# SETUP
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
TEST_DB_NAME = os.getenv('TEST_DB_NAME')

# We need an object oriented way to connect to and communicate with the database.
class Database(object): 
    # Constructor to make a connection to the database and return an object to execute queries with.
    def __init__(self, dbname, user, password, host, port):
        self.connection = psycopg2.connect(dbname = dbname, user = user, password = password, host = host, port = port)
        self.cursor = self.connection.cursor()
        self.connection_details = f"dbname={dbname} user={user} password={password} host={host} port={port}"
        self.create_tables()
        self.setup_test_data()

    # Methods to close connection and commit changes to the database.
    def close(self):
      self.connection.close()

    def commit(self):
      self.connection.commit()
        
    def create_tables(self): 
        s = """
        CREATE TABLE IF NOT EXISTS Hotel_Chain (
        chain_ID INT,
        name VARCHAR(50) NOT NULL,
        number_of_hotels INT NOT NULL,
        PRIMARY KEY (chain_ID)
        );

        CREATE TABLE IF NOT EXISTS Hotel (
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

        CREATE TABLE IF NOT EXISTS Employee (
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

        CREATE TABLE IF NOT EXISTS Employee_Role (
        employee_SSN_SIN INT,
        employee_ID INT,
        role VARCHAR(50) NOT NULL,
        PRIMARY KEY (employee_SSN_SIN, employee_ID, role),
        FOREIGN KEY (employee_SSN_SIN, employee_ID) REFERENCES Employee(employee_SSN_SIN, employee_ID) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS Hotel_Phone_Number (
        hotel_ID INT,
        phone_number VARCHAR(20),
        PRIMARY KEY (hotel_ID, phone_number),
        FOREIGN KEY (hotel_ID) REFERENCES Hotel(hotel_ID) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS Hotel_Chain_Central_Office_Address (
        chain_ID INT,
        address_street_name VARCHAR(50) NOT NULL,
        address_street_number INT NOT NULL,
        address_city VARCHAR(50) NOT NULL,
        address_province_state VARCHAR(50) NOT NULL,
        address_country VARCHAR(50) NOT NULL,
        PRIMARY KEY (chain_ID),
        FOREIGN KEY (chain_ID) REFERENCES Hotel_Chain(chain_ID) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS Hotel_Chain_Contact_Email (
        chain_ID INT,
        contact_email VARCHAR(50) NOT NULL,
        PRIMARY KEY (chain_ID),
        FOREIGN KEY (chain_ID) REFERENCES Hotel_Chain(chain_ID) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS Hotel_Chain_Phone_Number (
        chain_ID INT,
        phone_number VARCHAR(12),
        PRIMARY KEY (chain_ID, phone_number),
        FOREIGN KEY (chain_ID) REFERENCES Hotel_Chain(chain_ID) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS Room (
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

        CREATE TABLE IF NOT EXISTS Amenity (
        amenity_id INT,
        amenity_name VARCHAR(50)
        NOT NULL,
        PRIMARY KEY (amenity_id)
        );

        CREATE TABLE IF NOT EXISTS Has_Amenity (
        amenity_id INT,
        hotel_id INT,
        room_number INT,
        PRIMARY KEY (amenity_id, hotel_id, room_number),
        FOREIGN KEY (hotel_id, room_number) REFERENCES Room(hotel_ID, room_number) ON DELETE CASCADE,
        FOREIGN KEY (amenity_id) REFERENCES Amenity(amenity_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS Customer (
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

        CREATE TABLE IF NOT EXISTS Booking (
        booking_ID INT,
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

        CREATE TABLE IF NOT EXISTS Rental (
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
        FOREIGN KEY (customer_SSN_SIN) REFERENCES Customer(customer_SSN_SIN),
        FOREIGN KEY (employee_SSN_SIN, employee_ID) REFERENCES Employee(employee_SSN_SIN, employee_ID),
        FOREIGN KEY (booking_ID) REFERENCES Booking(booking_ID),
        FOREIGN KEY (room_number, hotel_ID) REFERENCES Room(room_number, hotel_ID) ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS Users (
        user_SSN_SIN INT PRIMARY KEY,
        password VARCHAR(1024) NOT NULL,
        role VARCHAR(10) NOT NULL,
        CHECK (role = 'customer' OR role = 'employee')
        ); 

        CREATE OR REPLACE VIEW hotel_total_room_capacity AS
        SELECT hotel_chain.name as hotel_chain_name, hotel.chain_id, hotel.hotel_id, room.room_number, room.room_capacity 
        FROM room 
        LEFT JOIN hotel ON room.hotel_id=hotel.hotel_id 
        LEFT JOIN hotel_chain on hotel_chain.chain_id=hotel.chain_id;

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
        """
        try:
            self.cursor.execute(s)
            self.commit()
        except Exception as e:
            self.connection.rollback()
            traceback.print_exc()
    
    def setup_test_data(self):
        # Insert sample data into the tables
        sample_data = """
        -- Insert data for Hotel_Chain table
        INSERT INTO Hotel_Chain (chain_ID, name, number_of_hotels) VALUES (1, 'Hilton', 0);
        INSERT INTO Hotel_Chain (chain_ID, name, number_of_hotels) VALUES (2, 'Marriott International', 0);
        INSERT INTO Hotel_Chain (chain_ID, name, number_of_hotels) VALUES (3, 'InterContinental Hotels Group', 0);
        INSERT INTO Hotel_Chain (chain_ID, name, number_of_hotels) VALUES (4, 'AccorHotels', 0);
        INSERT INTO Hotel_Chain (chain_ID, name, number_of_hotels) VALUES (5, 'Wyndham Hotels and Resorts', 0);

        -- Insert data for Hotel_Chain_Central_Office_Address, Hotel_Chain_Contact_Email, and Hotel_Chain_Phone_Number tables
        INSERT INTO Hotel_Chain_Central_Office_Address (chain_ID, address_street_name, address_street_number, address_city, address_province_state, address_country)
        VALUES (1, 'Park Ave', 123, 'New York', 'NY', 'USA');

        INSERT INTO Hotel_Chain_Central_Office_Address (chain_ID, address_street_name, address_street_number, address_city, address_province_state, address_country)
        VALUES (2, 'Fern Ave', 456, 'Bethesda', 'MD', 'USA');

        INSERT INTO Hotel_Chain_Central_Office_Address (chain_ID, address_street_name, address_street_number, address_city, address_province_state, address_country)
        VALUES (3, 'Park St', 789, 'Denham', 'Buckinghamshire', 'England');

        INSERT INTO Hotel_Chain_Central_Office_Address (chain_ID, address_street_name, address_street_number, address_city, address_province_state, address_country)
        VALUES (4, 'Rue de la Boétie', 159, 'Paris', 'Île-de-France', 'France');

        INSERT INTO Hotel_Chain_Central_Office_Address (chain_ID, address_street_name, address_street_number, address_city, address_province_state, address_country)
        VALUES (5, 'Broadway', 456, 'New York', 'NY', 'USA');

        INSERT INTO Hotel_Chain_Contact_Email (chain_ID, contact_email) VALUES (1, 'info@hilton.com');
        INSERT INTO Hotel_Chain_Phone_Number (chain_ID, phone_number) VALUES (1, '555-123-4567');

        INSERT INTO Hotel_Chain_Contact_Email (chain_ID, contact_email) VALUES (2, 'info@marriott.com');
        INSERT INTO Hotel_Chain_Phone_Number (chain_ID, phone_number) VALUES (2, '555-234-5678');

        INSERT INTO Hotel_Chain_Contact_Email (chain_ID, contact_email) VALUES (3, 'info@ihg.com');
        INSERT INTO Hotel_Chain_Phone_Number (chain_ID, phone_number) VALUES (3, '555-345-6789');

        INSERT INTO Hotel_Chain_Contact_Email (chain_ID, contact_email) VALUES (4, 'info@accorhotels.com');
        INSERT INTO Hotel_Chain_Phone_Number (chain_ID, phone_number) VALUES (4, '555-456-7890');

        INSERT INTO Hotel_Chain_Contact_Email (chain_ID, contact_email) VALUES (5, 'info@wyndham.com');
        INSERT INTO Hotel_Chain_Phone_Number (chain_ID, phone_number) VALUES (5, '555-567-8901');

        -- Hilton
        INSERT INTO Hotel
            (hotel_ID, chain_ID, number_of_rooms, address_street_name, address_street_number, address_city, address_province_state, address_country, contact_email, star_rating)
        VALUES
            (101, 1, 0, 'Main St', 2, 'New York', 'NY', 'USA', 'hilton1@example.com', 5),
            (102, 1, 0, 'Market St', 99, 'San Francisco', 'CA', 'USA', 'hilton2@example.com', 5),
            (103, 1, 0, 'Baker St', 25, 'London', 'England', 'UK', 'hilton3@example.com', 3),
            (104, 1, 0, 'King St', 45, 'Toronto', 'ON', 'Canada', 'hilton4@example.com', 4),
            (105, 1, 0, 'George St', 23, 'Sydney', 'NSW', 'Australia', 'hilton5@example.com', 5),
            (106, 1, 0, 'Queen St', 12, 'Auckland', 'Auckland', 'New Zealand', 'hilton6@example.com', 2),
            (107, 1, 0, 'Orchard Rd', 5, 'Singapore', 'Singapore', 'Singapore', 'hilton7@example.com', 5),
            (108, 1, 0, 'Las Ramblas', 23, 'Barcelona', 'Catalonia', 'Spain', 'hilton8@example.com', 4);

        -- Marriott 
        INSERT INTO Hotel
            (hotel_ID, chain_ID, number_of_rooms, address_street_name, address_street_number, address_city, address_province_state, address_country, contact_email, star_rating)
        VALUES
            (201, 2, 0, 'Madison Ave', 1, 'New York', 'NY', 'USA', 'marriott1@example.com', 5),
            (202, 2, 0, 'Mission St', 5, 'San Francisco', 'CA', 'USA', 'marriott2@example.com', 5),
            (203, 2, 0, 'Oxford St', 2, 'London', 'England', 'UK', 'marriott3@example.com', 3),
            (204, 2, 0, 'Front St', 7, 'Toronto', 'ON', 'Canada', 'marriott4@example.com', 4),
            (205, 2, 0, 'Pitt St', 3, 'Sydney', 'NSW', 'Australia', 'marriott5@example.com', 5),
            (206, 2, 0, 'Victoria St', 2, 'Auckland', 'Auckland', 'New Zealand', 'marriott6@example.com', 2),
            (207, 2, 0, 'Shenton Way', 8, 'Singapore', 'Singapore', 'Singapore', 'marriott7@example.com', 5),
            (208, 2, 0, 'Passeig de Gracia', 9, 'Barcelona', 'Catalonia', 'Spain', 'marriott8@example.com', 4);

        -- Intercontinental 
        INSERT INTO Hotel
            (hotel_ID, chain_ID, number_of_rooms, address_street_name, address_street_number, address_city, address_province_state, address_country, contact_email, star_rating)
        VALUES
            (301, 3, 0, 'Park Ave', 6, 'New York', 'NY', 'USA', 'intercontinental1@example.com', 5),
            (302, 3, 0, 'Van Ness Ave', 15, 'San Francisco', 'CA', 'USA', 'intercontinental2@example.com', 5),
            (303, 3, 0, 'Regent St', 16, 'London', 'England', 'UK', 'intercontinental3@example.com', 3),
            (304, 3, 0, 'Yonge St', 82, 'Toronto', 'ON', 'Canada', 'intercontinental4@example.com', 4),
            (305, 3, 0, 'Elizabeth St', 53, 'Sydney', 'NSW', 'Australia', 'intercontinental5@example.com', 5),
            (306, 3, 0, 'Wellesley St', 25, 'Auckland', 'Auckland', 'New Zealand', 'intercontinental6@example.com', 1),
            (307, 3, 0, 'Bukit Timah Rd', 14, 'Singapore', 'Singapore', 'Singapore', 'intercontinental7@example.com', 5),
            (308, 3, 0, 'Passeig de Gracia', 63, 'Barcelona', 'Catalonia', 'Spain', 'intercontinental8@example.com', 4);

        -- AccorHotels
        INSERT INTO Hotel
            (hotel_ID, chain_ID, number_of_rooms, address_street_name, address_street_number, address_city, address_province_state, address_country, contact_email, star_rating)
        VALUES
            (401, 4, 0, 'Fifth Ave', 97, 'New York', 'NY', 'USA', 'accor1@example.com', 5),
            (402, 4, 0, 'Geary St', 53, 'San Francisco', 'CA', 'USA', 'accor2@example.com', 5),
            (403, 4, 0, 'Coventry St', 25, 'London', 'England', 'UK', 'accor3@example.com', 4),
            (404, 4, 0, 'Queen St', 15, 'Toronto', 'ON', 'Canada', 'accor4@example.com', 3),
            (405, 4, 0, 'Pitt St', 97, 'Sydney', 'NSW', 'Australia', 'accor5@example.com', 5),
            (406, 4, 0, 'Albert St', 23, 'Auckland', 'Auckland', 'New Zealand', 'accor6@example.com', 1),
            (407, 4, 0, 'Cecil St', 68, 'Singapore', 'Singapore', 'Singapore', 'accor7@example.com', 5),
            (408, 4, 0, 'Rambla de Catalunya', 23, 'Barcelona', 'Catalonia', 'Spain', 'accor8@example.com', 4);

        --Wyndham
        INSERT INTO Hotel
            (hotel_ID, chain_ID, number_of_rooms, address_street_name, address_street_number, address_city, address_province_state, address_country, contact_email, star_rating)
        VALUES
            (501, 5, 0, 'Broadway', 15, 'New York', 'NY', 'USA', 'wyndham1@example.com', 5),
            (502, 5, 0, 'Fisherman''s Wharf', 64, 'San Francisco', 'CA', 'USA', 'wyndham2@example.com', 5),
            (503, 5, 0, 'Baker St', 96, 'London', 'England', 'UK', 'wyndham3@example.com', 4),
            (504, 5, 0, 'Queen St', 97, 'Toronto', 'ON', 'Canada', 'wyndham4@example.com', 3),
            (505, 5, 0, 'George St', 325, 'Sydney', 'NSW', 'Australia', 'wyndham5@example.com', 5),
            (506, 5, 0, 'Queen St', 64, 'Auckland', 'Auckland', 'New Zealand', 'wyndham6@example.com', 2),
            (507, 5, 0, 'Orchard Rd', 21, 'Singapore', 'Singapore', 'Singapore', 'wyndham7@example.com', 5),
            (508, 5, 0, 'Passeig de Gracia', 123, 'Barcelona', 'Catalonia', 'Spain', 'wyndham8@example.com', 4);

        -- Hotel phone numbers
        -- Hilton
        -- Hilton Hotel Phone Numbers
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (101, '+1-555-1234');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (102, '+1-555-2345');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (103, '+44-20-1234-5678');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (104, '+1-416-555-6789');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (105, '+61-2-555-7890');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (106, '+64-9-555-8901');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (107, '+65-6222-1234');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (108, '+34-93-567-8901');

        -- Marriott Hotel Phone Numbers
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (201, '+1-212-555-1234');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (202, '+1-415-555-2345');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (203, '+44-20-1234-5678');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (204, '+1-416-555-6789');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (205, '+61-2-555-7890');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (206, '+64-9-555-8901');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (207, '+65-6222-1234');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (208, '+34-93-567-8901');

        -- Intercontinental Hotel Phone Numbers
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (301, '+1-212-555-1234');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (302, '+1-415-555-2345');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (303, '+44-20-1234-5678');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (304, '+1-416-555-6789');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (305, '+61-2-555-7890');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (306, '+64-9-555-8901');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (307, '+65-6222-1234');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (308, '+34-93-567-8901');

        -- AccorHotels Phone Numbers
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (401, '+1-212-555-1234');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (402, '+1-415-555-2345');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (403, '+44-20-1234-5678');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (404, '+1-416-555-6789');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (405, '+61-2-555-7890');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (406, '+64-9-555-8901');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (407, '+65-6222-1234');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (408, '+34-93-567-8901');

        -- Wyndham Phone Numbers
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (501, '+1-212-555-1234');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (502, '+1-415-555-2345');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (503, '+44-20-1234-5678');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (504, '+1-416-555-6789');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (505, '+61-2-555-7890');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (506, '+64-9-555-8901');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (507, '+65-6222-1234');
        INSERT INTO Hotel_Phone_Number (hotel_ID, phone_number) VALUES (508, '+34-93-567-8901');

        -- Rooms
        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES (1, 103, 2, 'City', 300, TRUE, NULL),
            (2, 103, 2, 'Garden', 320, TRUE, NULL),
            (3, 103, 3, 'Pool', 350, FALSE, NULL),
            (4, 103, 4, 'City', 400, TRUE, NULL),
            (5, 103, 4, 'Garden', 420, FALSE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES (1, 104, 2, 'City', 320, TRUE, NULL),
            (2, 104, 3, 'Garden', 360, TRUE, NULL),
            (3, 104, 3, 'Pool', 380, FALSE, NULL),
            (4, 104, 4, 'City', 420, TRUE, NULL),
            (5, 104, 5, 'Garden', 500, FALSE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES (1, 105, 1, 'City', 100, TRUE, NULL),
            (2, 105, 2, 'Garden', 150, TRUE, NULL),
            (3, 105, 2, 'Pool', 170, FALSE, NULL),
            (4, 105, 3, 'City', 200, TRUE, NULL),
            (5, 105, 3, 'Garden', 220, FALSE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES (1, 106, 2, 'City', 250, TRUE, NULL),
            (2, 106, 3, 'Garden', 290, TRUE, NULL),
            (3, 106, 3, 'Pool', 320, FALSE, NULL),
            (4, 106, 4, 'City', 380, TRUE, NULL),
            (5, 106, 5, 'Garden', 450, FALSE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES (1, 107, 2, 'City', 320, TRUE, NULL),
            (2, 107, 2, 'Garden', 350, TRUE, NULL),
            (3, 107, 3, 'Pool', 400, FALSE, NULL),
            (4, 107, 4, 'City', 450, TRUE, NULL),
            (5, 107, 4, 'Garden', 500, FALSE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES
        (1, 108, 1, 'City', 75, TRUE, NULL),
        (2, 108, 2, 'Pool', 125, TRUE, NULL),
        (3, 108, 2, 'Garden', 125, TRUE, NULL),
        (4, 108, 3, 'City', 175, TRUE, NULL),
        (5, 108, 4, 'Pool', 225, FALSE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES
        (1, 201, 1, 'City', 50, TRUE, NULL),
        (2, 201, 2, 'Garden', 100, TRUE, NULL),
        (3, 201, 2, 'Pool', 100, TRUE, NULL),
        (4, 201, 3, 'City', 150, TRUE, NULL),
        (5, 201, 4, 'Garden', 200, FALSE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES
        (1, 202, 1, 'City', 55, TRUE, NULL),
        (2, 202, 2, 'Garden', 110, TRUE, NULL),
        (3, 202, 2, 'Pool', 110, TRUE, NULL),
        (4, 202, 3, 'City', 165, TRUE, NULL),
        (5, 202, 4, 'Garden', 220, FALSE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES
        (1, 203, 1, 'City', 45, TRUE, NULL),
        (2, 203, 2, 'Garden', 90, TRUE, NULL),
        (3, 203, 2, 'Pool', 90, TRUE, NULL),
        (4, 203, 3, 'City', 135, TRUE, NULL),
        (5, 203, 4, 'Garden', 180, FALSE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES
        (1, 204, 1, 'City', 60, TRUE, NULL),
        (2, 204, 2, 'Garden', 120, TRUE, NULL),
        (3, 204, 2, 'Pool', 120, TRUE, NULL),
        (4, 204, 3, 'City', 180, TRUE, NULL),
        (5, 204, 4, 'Garden', 240, FALSE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES
        (1, 205, 1, 'City', 75, TRUE, NULL),
        (2, 205, 2, 'Garden', 150, TRUE, NULL),
        (3, 205, 2, 'Pool', 150, TRUE, NULL),
        (4, 205, 3, 'City', 225, TRUE, NULL),
        (5, 205, 4, 'Garden', 300, FALSE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES
        (1, 206, 2, 'City', 120, TRUE, NULL),
        (2, 206, 4, 'Garden', 220, TRUE, NULL),
        (3, 206, 3, 'Pool', 180, FALSE, 'Leaky faucet'),
        (4, 206, 2, 'City', 120, FALSE, NULL),
        (5, 206, 1, 'City', 100, TRUE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES
        (1, 207, 3, 'Garden', 210, TRUE, NULL),
        (2, 207, 2, 'City', 140, TRUE, NULL),
        (3, 207, 4, 'Pool', 240, FALSE, 'Broken AC'),
        (4, 207, 1, 'City', 90, FALSE, 'No hot water'),
        (5, 207, 2, 'Garden', 160, TRUE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES
        (1, 208, 5, 'Pool', 350, TRUE, 'Stained carpet'),
        (2, 208, 2, 'City', 140, TRUE, NULL),
        (3, 208, 3, 'Garden', 210, FALSE, NULL),
        (4, 208, 4, 'Pool', 280, TRUE, NULL),
        (5, 208, 1, 'City', 90, TRUE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES
        (1, 301, 4, 'Garden', 280, TRUE, 'Clogged sink'),
        (2, 301, 2, 'City', 140, TRUE, NULL),
        (3, 301, 3, 'Pool', 210, FALSE, NULL),
        (4, 301, 5, 'Pool', 350, TRUE, NULL),
        (5, 301, 1, 'City', 90, TRUE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES
        (1, 302, 3, 'Garden', 210, TRUE, NULL),
        (2, 302, 2, 'City', 140, TRUE, NULL),
        (3, 302, 4, 'Pool', 280, FALSE, 'Leaky shower'),
        (4, 302, 1, 'City', 90, FALSE, NULL),
        (5, 302, 2, 'Garden', 160, TRUE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES
        (1, 303, 1, 'City', 100, TRUE, NULL),
        (2, 303, 2, 'City', 140, TRUE, NULL),
        (3, 303, 3, 'Pool', 210, FALSE, 'Noisy AC'),
        (4, 303, 4, 'Garden', 280, TRUE, NULL),
        (5, 303, 5, 'Pool', 350, FALSE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES
        (1, 304, 2, 'City', 140, TRUE, NULL),
        (2, 304, 4, 'Pool', 280, TRUE, NULL),
        (3, 304, 1, 'City', 90, FALSE, NULL),
        (4, 304, 3, 'Garden', 210, TRUE, NULL),
        (5, 304, 5, 'Pool', 350, FALSE, 'Broken TV');

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES (1, 305, 1, 'City', 50, TRUE, NULL),
            (2, 305, 2, 'Garden', 75, TRUE, NULL),
            (3, 305, 3, 'Pool', 100, FALSE, NULL),
            (4, 305, 4, 'City', 125, TRUE, NULL),
            (5, 305, 5, 'Garden', 150, FALSE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES (1, 306, 1, 'Pool', 50, TRUE, NULL),
            (2, 306, 2, 'City', 75, TRUE, NULL),
            (3, 306, 3, 'Garden', 100, FALSE, NULL),
            (4, 306, 4, 'Pool', 125, TRUE, NULL),
            (5, 306, 5, 'City', 150, FALSE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES (1, 307, 1, 'Garden', 50, TRUE, NULL),
            (2, 307, 2, 'Pool', 75, TRUE, NULL),
            (3, 307, 3, 'City', 100, FALSE, NULL),
            (4, 307, 4, 'Garden', 125, TRUE, NULL),
            (5, 307, 5, 'Pool', 150, FALSE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES (1, 308, 1, 'City', 50, TRUE, NULL),
            (2, 308, 2, 'Garden', 75, TRUE, NULL),
            (3, 308, 3, 'Pool', 100, FALSE, NULL),
            (4, 308, 4, 'City', 125, TRUE, NULL),
            (5, 308, 5, 'Garden', 150, FALSE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES (1, 401, 1, 'Pool', 50, TRUE, NULL),
            (2, 401, 2, 'City', 75, TRUE, NULL),
            (3, 401, 3, 'Garden', 100, FALSE, NULL),
            (4, 401, 4, 'Pool', 125, TRUE, NULL),
            (5, 401, 5, 'City', 150, FALSE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES (1, 402, 2, 'City', 80, TRUE, NULL),
            (2, 402, 4, 'Garden', 150, TRUE, NULL),
            (3, 402, 2, 'Pool', 100, TRUE, 'Leaky faucet'),
            (4, 402, 1, 'City', 60, FALSE, NULL),
            (5, 402, 3, 'Garden', 120, TRUE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES (1, 403, 1, 'City', 70, FALSE, 'Broken AC'),
            (2, 403, 2, 'Pool', 120, TRUE, NULL),
            (3, 403, 3, 'Garden', 160, TRUE, NULL),
            (4, 403, 2, 'City', 100, TRUE, NULL),
            (5, 403, 4, 'Garden', 200, TRUE, 'Clogged toilet');

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES (1, 404, 1, 'City', 50, FALSE, NULL),
            (2, 404, 2, 'Garden', 90, TRUE, NULL),
            (3, 404, 3, 'City', 130, TRUE, NULL),
            (4, 404, 4, 'Pool', 180, TRUE, NULL),
            (5, 404, 5, 'Garden', 250, TRUE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES (1, 405, 1, 'City', 60, FALSE, NULL),
            (2, 405, 2, 'Pool', 120, TRUE, 'TV not working'),
            (3, 405, 3, 'Garden', 160, TRUE, NULL),
            (4, 405, 2, 'City', 100, TRUE, NULL),
            (5, 405, 4, 'Garden', 200, TRUE, 'Leaky shower');

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES (1, 406, 1, 'City', 70, FALSE, NULL),
            (2, 406, 2, 'Garden', 120, TRUE, 'Broken hair dryer'),
            (3, 406, 3, 'City', 160, TRUE, NULL),
            (4, 406, 4, 'Pool', 200, TRUE, NULL),
            (5, 406, 5, 'Garden', 270, TRUE, 'Clogged sink');

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES (1, 407, 1, 'Garden', 75, TRUE, NULL),
        (2, 407, 2, 'Pool', 100, TRUE, NULL),
        (3, 407, 2, 'Garden', 100, FALSE, NULL),
        (4, 407, 3, 'Pool', 150, TRUE, NULL),
        (5, 407, 4, 'City', 200, FALSE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES (1, 408, 1, 'City', 75, TRUE, NULL),
        (2, 408, 2, 'Garden', 100, TRUE, NULL),
        (3, 408, 2, 'Pool', 100, FALSE, NULL),
        (4, 408, 3, 'Garden', 150, TRUE, NULL),
        (5, 408, 4, 'City', 200, FALSE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems) VALUES
        (1, 501, 1, 'Garden', 75, TRUE, NULL),
        (2, 501, 2, 'City', 100, TRUE, NULL),
        (3, 501, 2, 'Garden', 100, FALSE, NULL),
        (4, 501, 3, 'City', 150, TRUE, NULL),
        (5, 501, 4, 'Pool', 200, FALSE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems) VALUES
        (1, 502, 1, 'Pool', 75, TRUE, NULL),
        (2, 502, 2, 'City', 100, TRUE, NULL),
        (3, 502, 2, 'Garden', 100, FALSE, NULL),
        (4, 502, 3, 'City', 150, TRUE, NULL),
        (5, 502, 4, 'Pool', 200, FALSE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems) VALUES
        (1, 503, 1, 'Garden', 50, TRUE, NULL),
        (2, 503, 2, 'City', 75, TRUE, NULL),
        (3, 503, 2, 'Garden', 75, FALSE, NULL),
        (4, 503, 3, 'Pool', 125, TRUE, NULL),
        (5, 503, 4, 'City', 175, FALSE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems) VALUES
        (1, 504, 1, 'City', 50, TRUE, NULL),
        (2, 504, 2, 'Garden', 75, TRUE, NULL),
        (3, 504, 2, 'Pool', 75, FALSE, NULL),
        (4, 504, 3, 'City', 125, TRUE, NULL),
        (5, 504, 4, 'Garden', 175, FALSE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems) VALUES
        (1, 505, 1, 'Pool', 50, TRUE, NULL),
        (2, 505, 2, 'Garden', 75, TRUE, NULL),
        (3, 505, 2, 'City', 75, FALSE, NULL),
        (4, 505, 3, 'Garden', 125, TRUE, NULL),
        (5, 505, 4, 'Pool', 175, FALSE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES
            (1, 506, 1, 'City', 60, FALSE, NULL),
            (2, 506, 2, 'City', 80, TRUE, NULL),
            (3, 506, 2, 'Garden', 100, TRUE, NULL),
            (4, 506, 4, 'Garden', 160, TRUE, NULL),
            (5, 506, 4, 'Pool', 200, FALSE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES
            (1, 507, 2, 'City', 120, TRUE, NULL),
            (2, 507, 2, 'Garden', 140, FALSE, NULL),
            (3, 507, 3, 'Garden', 180, TRUE, NULL),
            (4, 507, 4, 'Pool', 240, TRUE, NULL),
            (5, 507, 5, 'Pool', 300, FALSE, NULL);

        INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems)
        VALUES
            (1, 508, 1, 'City', 70, FALSE, NULL),
            (2, 508, 2, 'City', 100, TRUE, NULL),
            (3, 508, 3, 'Garden', 150, TRUE, NULL),
            (4, 508, 4, 'Pool', 220, TRUE, NULL),
            (5, 508, 5, 'Pool', 300, FALSE, NULL);
        """
        try:
            self.cursor.execute(sample_data)
            self.commit()
        except Exception as e:
            traceback.print_exc()
            self.connection.rollback()
    
    def clear_table(self, table_name):
        try:
            # Clear the table
            self.cursor.execute(f"DELETE FROM {table_name}")
            self.commit()
            print(f"{table_name} table cleared.")

        except Exception as e:
            print(f"Error clearing {table_name} table:", e)
            self.connection.rollback()

    ### Action methods on the database.
    # Method checks whether a user exists and returns their role if they exist.
    def check_account_and_role(self, ssn_sin, password, role):
        self.cursor.execute("SELECT * FROM Users WHERE user_SSN_SIN=%s", (ssn_sin,))
        result = self.cursor.fetchone()

        if not result:
            return ["Invalid SSN/SIN"]
        hashed_pass = result[1]

        if check_password_hash(hashed_pass, password):
            user_type = result[2]
            if user_type == role:
                if user_type == "customer":
                    self.cursor.execute("SELECT * FROM Customer WHERE customer_SSN_SIN=%s", (ssn_sin,))
                elif user_type == "employee":
                    self.cursor.execute("SELECT * FROM Employee WHERE employee_SSN_SIN=%s", (ssn_sin,))
                
                user_info = self.cursor.fetchone()
                return ["Found User", user_type, user_info]
            else:
                return ["Invalid Role"]
        else:
            return ["Invalid Password"]

    def get_all_hotels(self):
        self.cursor.execute("SELECT * FROM Hotel")
        results = self.cursor.fetchall()
        return results

    def get_hotel(self, id):
        self.cursor.execute("SELECT * FROM Hotel WHERE hotel_ID = %s", (id,))
        results = self.cursor.fetchone()
        return results

    def get_all_hotel_chains(self):
        self.cursor.execute("SELECT * FROM Hotel_Chain")
        results = self.cursor.fetchall()
        return results

    def get_hotel_chain(self, chain_id=None, name=None):
        if chain_id is not None and name is not None:
            self.cursor.execute("""
                SELECT * FROM Hotel_Chain 
                WHERE chain_ID = %s OR name = %s
            """, (chain_id, name))
        elif chain_id is not None:
            self.cursor.execute("SELECT * FROM Hotel_Chain WHERE chain_ID = %s", (chain_id,))
        elif name is not None:
            self.cursor.execute("SELECT * FROM Hotel_Chain WHERE name = %s", (name,))
        else:
            raise ValueError("Either chain_id or name must be provided.")

        results = self.cursor.fetchall()
        return results

    def get_employees_by_hotel_id(self, hotel_id):
        self.cursor.execute("SELECT * FROM Employee WHERE hotel_ID = %s", (hotel_id,))
        results = self.cursor.fetchall()
        return results

    def get_all_employees(self): 
      self.cursor.execute("SELECT * FROM Employee")
      results = self.cursor.fetchall()
      return results

    def get_employee(self, employee_ssn_sin, employee_id=None):
        if employee_id is None:
            self.cursor.execute("SELECT * FROM Employee WHERE employee_SSN_SIN = %s", (employee_ssn_sin,))
        else:
            self.cursor.execute("SELECT * FROM Employee WHERE employee_SSN_SIN = %s AND employee_ID = %s", (employee_ssn_sin, employee_id))
        results = self.cursor.fetchone()
        return results

    def get_employee_roles(self, employee_SSN_SIN, employee_ID):
        self.cursor.execute("SELECT role FROM Employee_Role WHERE Employee_Role.employee_SSN_SIN=%s AND Employee_Role.employee_ID=%s", (employee_SSN_SIN, employee_ID))
        result = self.cursor.fetchall()

        roles = [row[0].lower().strip() for row in result]

        return roles

    def get_all_hotel_phone_numbers(self):
        self.cursor.execute("SELECT * FROM Hotel_Phone_Number")
        results = self.cursor.fetchall()
        return results

    def get_hotel_phone_number(self, hotel_id):
        self.cursor.execute("SELECT * FROM Hotel_Phone_Number WHERE hotel_ID = %s", (hotel_id,))
        results = self.cursor.fetchall()
        return results

    def get_all_hotel_chain_central_office_addresses(self):
        self.cursor.execute("SELECT * FROM Hotel_Chain_Central_Office_Address")
        results = self.cursor.fetchall()
        return results

    def get_hotel_chain_central_office_address(self, chain_id):
        self.cursor.execute("SELECT * FROM Hotel_Chain_Central_Office_Address WHERE chain_ID = %s", (chain_id,))
        results = self.cursor.fetchall()
        return results

    def get_all_hotel_chain_contact_emails(self):
        self.cursor.execute("SELECT * FROM Hotel_Chain_Contact_Email")
        results = self.cursor.fetchall()
        return results

    def get_hotel_chain_contact_email(self, chain_id):
        self.cursor.execute("SELECT * FROM Hotel_Chain_Contact_Email WHERE chain_ID = %s", (chain_id,))
        results = self.cursor.fetchall()
        return results

    def get_all_hotel_chain_phone_numbers(self):
        self.cursor.execute("SELECT * FROM Hotel_Chain_Phone_Number")
        results = self.cursor.fetchall()
        return results

    def get_hotel_chain_phone_number(self, chain_id):
        self.cursor.execute("SELECT * FROM Hotel_Chain_Phone_Number WHERE chain_ID = %s", (chain_id,))
        results = self.cursor.fetchall()
        return results
    
    def get_all_rooms_with_hotel_info(self):
        self.cursor.execute("SELECT * FROM ROOM LEFT JOIN hotel on room.hotel_id = hotel.hotel_id")
        results = self.cursor.fetchall()
        return results

    def get_all_rooms(self):
        self.cursor.execute("SELECT * FROM Room")
        results = self.cursor.fetchall()
        return results

    def get_room(self, room_number, hotel_id):
        self.cursor.execute("SELECT * FROM Room WHERE room_number = %s AND hotel_ID = %s", (room_number, hotel_id))
        results = self.cursor.fetchone()
        return results

    def get_all_amenities(self):
        self.cursor.execute("SELECT * FROM Amenity")
        results = self.cursor.fetchall()
        return results

    def get_customer(self, customer_ssn_sin):
        self.cursor.execute("SELECT * FROM Customer WHERE customer_SSN_SIN = %s", (customer_ssn_sin,))
        results = self.cursor.fetchall()
        return results
    
    def get_all_customers(self):
        self.cursor.execute("SELECT * FROM Customer")
        results = self.cursor.fetchall()
        return results

    def get_all_bookings(self, ssn_sin=None):
        if ssn_sin is None:
            self.cursor.execute("SELECT * FROM Booking WHERE canceled = false")
        else:
            self.cursor.execute("SELECT * FROM Booking WHERE customer_SSN_SIN = %s AND canceled = false", (ssn_sin,))
        
        results = self.cursor.fetchall()
        return results
        
    def get_booking(self, booking_id):
        self.cursor.execute("SELECT * FROM Booking WHERE booking_ID = %s AND canceled = FALSE", (booking_id,))
        results = self.cursor.fetchone()
        return results

    def get_all_rentals(self):
        self.cursor.execute("SELECT * FROM Rental")
        results = self.cursor.fetchall()
        return results

    def get_rental(self, rental_id):
        self.cursor.execute("SELECT * FROM Rental WHERE rental_ID = %s", (rental_id,))
        results = self.cursor.fetchall()
        return results
    
    def get_rentals_by_customer(self, customer_SSN_SIN):
        self.cursor.execute("SELECT * FROM Rental WHERE customer_SSN_SIN = %s", (customer_SSN_SIN,))
        results = self.cursor.fetchall()
        return results

    ### INSERTION & UPDATION FUNCTIONS
    def insert_hotel(self, hotel_id, chain_id=None, number_of_rooms=None, address_street_name=None, address_street_number=None, 
                    address_city=None, address_province_state=None, address_country=None, contact_email=None, star_rating=None):
        try:
            # Check if the hotel already exists
            existing_hotel = self.get_hotel(hotel_id)
            if existing_hotel:
                # Update the hotel information if it exists
                update_query = "UPDATE Hotel SET "
                update_values = []

                # Create a dictionary with column names and parameter values
                columns_and_values = {
                    "chain_ID": chain_id,
                    "number_of_rooms": number_of_rooms,
                    "address_street_name": address_street_name,
                    "address_street_number": address_street_number,
                    "address_city": address_city,
                    "address_province_state": address_province_state,
                    "address_country": address_country,
                    "contact_email": contact_email,
                    "star_rating": star_rating
                }

                # Iterate through the dictionary and build the query
                for column, value in columns_and_values.items():
                    if value is not None:
                        update_query += f"{column} = %s, "
                        update_values.append(value)

                # Remove the trailing comma and space
                update_query = update_query.rstrip(', ')
                update_query += " WHERE hotel_ID = %s"
                update_values.append(hotel_id)

                self.cursor.execute(update_query, tuple(update_values))
            else:
                # Insert a new hotel if it doesn't exist
                self.cursor.execute("""
                    INSERT INTO Hotel (hotel_ID, chain_ID, number_of_rooms, address_street_name, address_street_number, 
                                      address_city, address_province_state, address_country, contact_email, star_rating) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (hotel_id, chain_id, number_of_rooms, address_street_name, address_street_number, 
                          address_city, address_province_state, address_country, contact_email, star_rating))
            self.commit()
        except Exception as e:
            self.connection.rollback()
            raise e


    def insert_hotel_chain(self, chain_id, name=None, number_of_hotels=None):
        try:
            # Check if the hotel chain already exists
            existing_hotel_chain = self.get_hotel_chain(chain_id)
            if existing_hotel_chain:
                # Update the hotel chain information if it exists
                update_query = "UPDATE Hotel_Chain SET "
                update_values = []

                # Create a dictionary with column names and parameter values
                columns_and_values = {
                    "name": name,
                    "number_of_hotels": number_of_hotels
                }

                # Iterate through the dictionary and build the query
                for column, value in columns_and_values.items():
                    if value is not None:
                        update_query += f"{column} = %s, "
                        update_values.append(value)

                # Remove the trailing comma and space
                update_query = update_query.rstrip(', ')
                update_query += " WHERE chain_ID = %s"
                update_values.append(chain_id)

                self.cursor.execute(update_query, tuple(update_values))
            else:
                # Insert a new hotel chain if it doesn't exist
                self.cursor.execute("INSERT INTO Hotel_Chain (chain_ID, name, number_of_hotels) VALUES (%s, %s, %s)",
                                    (chain_id, name, number_of_hotels))
            self.commit()
        except Exception as e:
            self.connection.rollback()
            raise e


    def insert_customer(self, customer_SSN_SIN, password, first_name, last_name, address_street_name, address_street_number, address_city, address_province_state, address_country, registration_date):
        try:
            # Check if the customer already exists in the Customer table or an employee exists with the same SSN_SIN
            existing_customer = self.get_customer(customer_SSN_SIN)
            existing_employee = self.get_employee(customer_SSN_SIN)

            if existing_customer or existing_employee:
                return (False, "Error: Customer or Employee with the same SSN/SIN already exists.")

            else:
                # Insert a new customer
                self.cursor.execute("INSERT INTO Customer (customer_SSN_SIN, first_name, last_name, address_street_name, address_street_number, address_city, address_province_state, address_country, registration_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                    (customer_SSN_SIN, first_name, last_name, address_street_name, address_street_number, address_city, address_province_state, address_country, registration_date))
                # Insert a new user
                self.cursor.execute("INSERT INTO Users (user_SSN_SIN, password, role) VALUES (%s, %s, %s)", (customer_SSN_SIN, password, 'customer'))
                self.commit()

        except Exception as e:
            self.connection.rollback()
            return (False, f"Error inserting customer: {e}")

        return (True, "Customer successfully registered.")


    def insert_employee(self, employee_SSN_SIN, employee_ID, password, first_name, last_name, address_street_name, address_street_number, address_city, address_province_state, address_country, hotel_ID, is_manager):
        try:
            # Check if the employee already exists in the Employee table or an customer exists with the same SSN_SIN
            existing_customer = self.get_customer(employee_SSN_SIN)
            existing_employee = self.get_employee(employee_SSN_SIN)

            if existing_employee or existing_customer:
                return (False, "Error: Customer or Employee with the same SSN/SIN already exists.")

            else:
                # Insert a new employee
                self.cursor.execute("INSERT INTO Employee (employee_SSN_SIN, employee_ID, first_name, last_name, address_street_name, address_street_number, address_city, address_province_state, address_country, hotel_ID, is_manager) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                    (employee_SSN_SIN, employee_ID, first_name, last_name, address_street_name, address_street_number, address_city, address_province_state, address_country, hotel_ID, is_manager))
                # Insert a new user
                self.cursor.execute("INSERT INTO Users (user_SSN_SIN, password, role) VALUES (%s, %s, %s)", (employee_SSN_SIN, password, 'employee'))
                self.commit()

        except Exception as e:
            self.connection.rollback()
            return (False, f"Error inserting employee: {e}")
        
        return (True, "Employee successfully registered")


    def insert_employee_role(self, employee_SSN_SIN, employee_ID, role):
        try:
            # Check if the Employee_Role entry already exists with the same employee and role
            self.cursor.execute(
                "SELECT COUNT(*) FROM Employee_Role WHERE employee_SSN_SIN = %s AND employee_ID = %s AND role = %s",
                (employee_SSN_SIN, employee_ID, role)
            )
            count = self.cursor.fetchone()[0]

            if count > 0:
                return (False, "Error: Employee already possesses the role.")
            else:
                # Insert a new employee role
                self.cursor.execute(
                    "INSERT INTO Employee_Role (employee_SSN_SIN, employee_ID, role) VALUES (%s, %s, %s)",
                    (employee_SSN_SIN, employee_ID, role)
                )
                self.connection.commit()
                return (True, "Employee role succesfully added.")
        except Exception as e:
            self.connection.rollback()
            return (False, f"Error adding employee role: {e}")
    

    def update_employee(self, employee_SSN_SIN, employee_ID=None, first_name=None, last_name=None, address_street_name=None, 
                        address_street_number=None, address_city=None, address_province_state=None, 
                        address_country=None, hotel_ID=None, promote_to_manager=None, demote_from_manager=None):

        if promote_to_manager is not None and demote_from_manager is not None:
            return "Error: Both promote_to_manager and demote_from_manager cannot be set at the same time."

        try:
            # Check if the employee exists
            existing_employee = self.get_employee(employee_SSN_SIN)

            if not existing_employee:
                return (False, "Error: Employee does not exist.")

            update_query = "UPDATE Employee SET "
            update_values = []

            # Create a dictionary with column names and parameter values
            columns_and_values = {
                "first_name": first_name,
                "last_name": last_name,
                "employee_ID": employee_ID,
                "address_street_name": address_street_name,
                "address_street_number": address_street_number,
                "address_city": address_city,
                "address_province_state": address_province_state,
                "address_country": address_country,
                "hotel_ID": hotel_ID,
            }

            # Iterate through the dictionary and build the query
            for column, value in columns_and_values.items():
                if value is not None:
                    update_query += f"{column} = %s, "
                    update_values.append(value)

            if promote_to_manager:
                update_query += "is_manager = %s, "
                update_values.append(True)
            else:
                update_query += "is_manager = %s, "
                update_values.append(False)

            # Check if any values were added to the query
            if len(update_values) == 0:
                return (False, "Error: No values provided to update.")

            # Remove the trailing comma and space
            update_query = update_query.rstrip(', ')
            update_query += " WHERE employee_SSN_SIN = %s"
            update_values.append(employee_SSN_SIN)

            self.cursor.execute(update_query, tuple(update_values))
            self.commit()
            return (True, "Employee updated successfully.")

        except Exception as e:
            self.connection.rollback()
            return (False, f"Error updating employee: {e}")

    
    def insert_room(self, room_number, hotel_id, room_capacity=None, view_type=None, price_per_night=None, is_extendable=None, room_problems=None):
        try:
            # Check if the room already exists
            existing_room = self.get_room(room_number, hotel_id)
            if existing_room:
                # Update the room information if it exists
                update_query = "UPDATE Room SET "
                update_values = []

                # Create a dictionary with column names and parameter values
                columns_and_values = {
                    "room_capacity": room_capacity,
                    "view_type": view_type,
                    "price_per_night": price_per_night,
                    "is_extendable": is_extendable,
                    "room_problems": room_problems
                }

                # Iterate through the dictionary and build the query
                for column, value in columns_and_values.items():
                    if value is not None:
                        update_query += f"{column} = %s, "
                        update_values.append(value)

                # Remove the trailing comma and space
                update_query = update_query.rstrip(', ')
                update_query += " WHERE room_number = %s AND hotel_ID = %s"
                update_values.append(room_number)
                update_values.append(hotel_id)

                self.cursor.execute(update_query, tuple(update_values))
            else:
                # Insert a new room if it doesn't exist
                self.cursor.execute("""
                    INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (room_number, hotel_id, room_capacity, view_type, price_per_night, is_extendable, room_problems))
            self.commit()
        except Exception as e:
            self.connection.rollback()
            raise e


    def insert_booking(self, customer_SSN_SIN, room_number, hotel_id, check_in_date, check_out_date):
        if check_in_date >= check_out_date:
            raise Exception("Error: Check-in date must be earlier than check-out date.")

        if check_in_date + datetime.timedelta(days=0) == check_out_date:
            raise Exception("Error: Check-in date and check-out date cannot be the same day.")

        try:
            # Check if the customer exists
            existing_customer = self.get_customer(customer_SSN_SIN)
            if not existing_customer:
                raise Exception("Error: Customer does not exist.")

            # Check if the room exists
            existing_room = self.get_room(room_number, hotel_id)
            if not existing_room:
                raise Exception("Error: Room does not exist.")

            # Check for duplicate bookings
            self.cursor.execute("""
                SELECT * FROM Booking 
                WHERE room_number = %s
                AND hotel_ID = %s
                AND (
                    (scheduled_check_in_date <= %s AND scheduled_check_out_date >= %s) 
                    OR (scheduled_check_out_date >= %s AND scheduled_check_out_date <= %s) 
                    OR (scheduled_check_in_date >= %s AND scheduled_check_in_date <= %s)
                )
                AND canceled = False
            """, (room_number, hotel_id, check_in_date, check_out_date, check_in_date, check_out_date, check_in_date, check_out_date))

            existing_booking = self.cursor.fetchone()
            if existing_booking:
                raise Exception("Error: Duplicate booking found.")

            # Insert the booking
            self.cursor.execute("""
                INSERT INTO Booking (booking_date, scheduled_check_in_date, scheduled_check_out_date, canceled, customer_SSN_SIN, room_number, hotel_ID, booking_id) 
                VALUES (%s, %s, %s, false, %s, %s, %s, %s)
            """, (datetime.date.today(), check_in_date, check_out_date, customer_SSN_SIN, room_number, hotel_id, randint(1, 1000000000)))
            self.commit()

        except Exception as e:
            self.connection.rollback()
            raise e
    

    def update_booking(self, booking_id, customer_SSN_SIN=None, room_number=None, hotel_id=None, check_in_date=None, check_out_date=None):
        try:
            # Check if the booking exists
            existing_booking = self.get_booking(booking_id)
            if not existing_booking:
                raise Exception("Error: Booking does not exist.")

            # Build the update query
            update_query = "UPDATE Booking SET "
            update_values = []

            # Create a dictionary with column names and parameter values
            columns_and_values = {
                "customer_SSN_SIN": customer_SSN_SIN,
                "room_number": room_number,
                "hotel_ID": hotel_id,
                "scheduled_check_in_date": check_in_date,
                "scheduled_check_out_date": check_out_date
            }

            # Iterate through the dictionary and build the query
            for column, value in columns_and_values.items():
                if value is not None:
                    update_query += f"{column} = %s, "
                    update_values.append(value)

            # Remove the trailing comma and space
            update_query = update_query.rstrip(', ')
            update_query += " WHERE booking_ID = %s"
            update_values.append(booking_id)

            # Execute the update query
            self.cursor.execute(update_query, tuple(update_values))
            self.commit()

        except Exception as e:
            self.connection.rollback()
            raise e
    

    def convert_booking_to_rental(self, booking_id, employee_ssn_sin, employee_id, total_paid=None, discount=None, additional_charges=None):
        try:
            # Check if the booking exists and is not canceled
            existing_booking = self.get_booking(booking_id)
            if not existing_booking or existing_booking[4]:
                return (False, "Error: Booking does not exist or has been canceled.")

            # Create the rental
            rental_data = {
                'base_price': self.get_room(existing_booking[6], existing_booking[7])[4],
                'date_paid': datetime.date.today(),
                'total_paid': 0 if total_paid is None else total_paid,
                'discount': 0 if discount is None else discount,
                'additional_charges': 0 if additional_charges is None else additional_charges,
                'check_in_date': existing_booking[2],
                'check_out_date': existing_booking[3],
                'customer_SSN_SIN': existing_booking[5],
                'booking_ID': existing_booking[0],
                'room_number': existing_booking[6],
                'hotel_ID': existing_booking[7],
                'employee_ID': employee_id,
                'employee_SSN_SIN': employee_ssn_sin
            }
            self.cursor.execute("""
                INSERT INTO Rental (base_price, date_paid, total_paid, discount, additional_charges, check_in_date, check_out_date, customer_SSN_SIN, booking_ID, room_number, hotel_ID, employee_ID, employee_SSN_SIN)
                VALUES (%(base_price)s, %(date_paid)s, %(total_paid)s, %(discount)s, %(additional_charges)s, %(check_in_date)s, %(check_out_date)s, %(customer_SSN_SIN)s, %(booking_ID)s, %(room_number)s, %(hotel_ID)s, %(employee_ID)s, %(employee_SSN_SIN)s)
            """, rental_data)
            self.commit()

            return (True, "Booking converted to rental successfully.")

        except Exception as e:
            self.connection.rollback()
            return (False, f"Error converting booking: {e}")


    def create_rental(self, employee_ssn_sin, employee_id, room_number, hotel_id, customer_SSN_SIN, check_in_date, check_out_date, total_paid=None, discount=None, additional_charges=None):
        if check_in_date >= check_out_date:
            return (False, "Error: Check-in date must be earlier than check-out date.")

        if check_in_date + datetime.timedelta(days=1) == check_out_date:
            return (False, "Error: Check-in date and check-out date cannot be the same day.")
        
        # if not check_employee_belongs_to_hotel(employee_ssn_sin, employee_id, hotel_id): 
        #    return (False, "Error: Employee is not authorized to create a rental for this hotel.")
        
        try:
            # Check if the customer exists
            existing_customer = self.get_customer(customer_SSN_SIN)
            if not existing_customer:
                return (False, "Error: Customer does not exist.")

            # Check if the room exists
            existing_room = self.get_room(room_number, hotel_id)
            if not existing_room:
                return (False, "Error: Room does not exist.")

            # Check for overlapping bookings
            self.cursor.execute("""
                SELECT * FROM Booking 
                WHERE room_number = %s
                AND hotel_ID = %s
                AND (
                    (scheduled_check_in_date <= %s AND scheduled_check_out_date >= %s) 
                    OR (scheduled_check_out_date >= %s AND scheduled_check_in_date <= %s) 
                    OR (scheduled_check_in_date >= %s AND scheduled_check_in_date <= %s)
                )
                AND canceled = false
            """, (room_number, hotel_id, check_in_date, check_out_date, check_in_date, check_out_date, check_in_date, check_out_date))
            
            overlapping_booking = self.cursor.fetchone()
            if overlapping_booking:
                return (False, "Error: Overlapping booking found.")
            
            # Check for overlapping rentals
            self.cursor.execute("""
                SELECT * FROM Rental 
                WHERE room_number = %s
                AND hotel_ID = %s
                AND (
                    (check_in_date <= %s AND check_out_date >= %s) 
                    OR (check_out_date >= %s AND check_out_date <= %s) 
                    OR (check_in_date >= %s AND check_in_date <= %s)
                )
            """, (room_number, hotel_id, check_in_date, check_out_date, check_in_date, check_out_date, check_in_date, check_out_date))
            
            existing_rental = self.cursor.fetchone()
            if existing_rental:
                return (False, "Error: Overlapping rental found.")

            # Create the rental
            rental_data = {
                'base_price': existing_room[4],
                'date_paid': datetime.date.today(),
                'total_paid': 0 if total_paid is None else total_paid,
                'discount': 0 if discount is None else discount,
                'additional_charges': 0 if additional_charges is None else additional_charges,
                'check_in_date': check_in_date,
                'check_out_date': check_out_date,
                'customer_SSN_SIN': customer_SSN_SIN,
                'booking_ID': None,
                'room_number': room_number,
                'hotel_ID': hotel_id,
                'employee_ID': employee_id,
                'employee_SSN_SIN': employee_ssn_sin
            }
            self.cursor.execute("""
                INSERT INTO Rental (base_price, date_paid, total_paid, discount, additional_charges, check_in_date, check_out_date, customer_SSN_SIN, booking_ID, room_number, hotel_ID, employee_ID, employee_SSN_SIN)
                VALUES (%(base_price)s, %(date_paid)s, %(total_paid)s, %(discount)s, %(additional_charges)s, %(check_in_date)s, %(check_out_date)s, %(customer_SSN_SIN)s, %(booking_ID)s, %(room_number)s, %(hotel_ID)s, %(employee_ID)s, %(employee_SSN_SIN)s)
            """, rental_data)
            self.commit()

            return (True, f"Rental created successfully.")

        except Exception as e:
            self.connection.rollback()
            return (False, f"Error creating rental:{e}")

    def get_all_hotels(self):
        query = """
        SELECT h.hotel_ID, h.chain_ID, h.number_of_rooms, h.address_street_name, h.address_street_number, 
            h.address_city, h.address_province_state, h.address_country, h.contact_email, h.star_rating
            FROM Hotel h;
        """

        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        hotels = []
        for row in rows:
            hotels.append({  
              "hotel_id": row[0],
              "chain_id": row[1],
              "number_of_rooms": row[2],
              "address_street_name": row[3],
              "address_street_number": row[4],
              "address_city": row[5],
              "address_province_state": row[6],
              "address_country": row[7],
              "contact_email": row[8],
              "star_rating": row[9]
            })

        return hotels

    # ONLY RETURNS HOTELS THAT HAVE ROOMS
    def search_hotels_and_rooms(self, start_date, end_date, hotel_chain=None, city=None, star_rating=None, view_type=None, room_capacity=None, is_extendable=None, price_per_night=None):
        query = """
        SELECT hc.name, hc.chain_id, h.hotel_ID, h.chain_ID, h.number_of_rooms, h.address_street_name, h.address_street_number, 
            h.address_city, h.address_province_state, h.address_country, h.contact_email, h.star_rating, 
            r.room_number, r.room_capacity, r.view_type, r.price_per_night, r.is_extendable, r.room_problems
            FROM Hotel h
            JOIN Room r ON h.hotel_ID = r.hotel_ID
            JOIN Hotel_Chain hc ON h.chain_ID = hc.chain_ID
            WHERE 1 = 1
            AND NOT EXISTS (
                SELECT 1
                FROM Booking b
                WHERE b.room_number = r.room_number
                AND b.hotel_ID = h.hotel_ID
                AND NOT (b.scheduled_check_out_date <= %(start_date)s OR b.scheduled_check_in_date >= %(end_date)s)
                AND b.canceled = false
            )
            AND NOT EXISTS (
                SELECT 1
                FROM Rental rt
                WHERE rt.room_number = r.room_number
                AND rt.hotel_ID = h.hotel_ID
                AND NOT (rt.check_out_date <= %(start_date)s OR rt.check_in_date >= %(end_date)s)
            )
        """

        params = {
            'start_date': start_date,
            'end_date': end_date
        }

        if hotel_chain is not None:
            query += " AND hc.name = %(hotel_chain)s"
            params['hotel_chain'] = hotel_chain

        if city is not None:
            query += " AND LOWER(h.address_city) LIKE LOWER(%(city)s)"
            params['city'] = f"%{city}%"

        if star_rating is not None:
            query += " AND h.star_rating = %(star_rating)s"
            params['star_rating'] = star_rating

        if view_type is not None:
            query += " AND r.view_type = %(view_type)s"
            params['view_type'] = view_type

        if room_capacity is not None:
            query += " AND r.room_capacity = %(room_capacity)s"
            params['room_capacity'] = room_capacity

        if is_extendable is not None:
            query += " AND r.is_extendable = %(is_extendable)s"
            params['is_extendable'] = is_extendable

        if price_per_night is not None:
            query += " AND r.price_per_night <= %(price_per_night)s"
            params['price_per_night'] = price_per_night

        query += " ORDER BY hc.name, h.hotel_ID, r.room_number"

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()

        hotels = {}

        for row in rows:
            chain_id = row[1]
            chain_name = row[0]
            hotel_id = row[2]

            if chain_id not in hotels:
                hotels[chain_id] = {
                    'chain_ID': chain_id,
                    'chain_name': chain_name,
                    'hotels': []
                }

            hotel = next((x for x in hotels[chain_id]['hotels'] if x['hotel_ID'] == hotel_id), None)
            if not hotel:
                hotel = {
                    'chain_id': chain_id,
                    'hotel_ID': hotel_id,
                    'number_of_rooms': row[4],
                    'address_street_name': row[5],
                    'address_street_number': row[6],
                    'address_city': row[7],
                    'address_province_state': row[8],
                    'address_country': row[9],
                    'contact_email': row[10],
                    'star_rating': row[11],
                    'rooms': []
                }
                hotels[chain_id]['hotels'].append(hotel)

            hotel['rooms'].append({
                'room_number': row[12],
                'room_capacity': row[13],
                'view_type': row[14],
                'price_per_night': row[15],
                'is_extendable': row[16],
                'room_problems': row[17]
            })

        return list(hotels.values())
    

    def update_customer(self, customer_SSN_SIN, first_name=None, last_name=None, address_street_name=None, address_street_number=None, address_city=None, address_province_state=None, address_country=None):
        try:
            columns_and_values = {
                "first_name": first_name,
                "last_name": last_name,
                "address_street_name": address_street_name,
                "address_street_number": address_street_number,
                "address_city": address_city,
                "address_province_state": address_province_state,
                "address_country": address_country
            }

            # Check if any values were passed in
            if all(v is None for v in columns_and_values.values()):
                return "Error: No values provided to update."

            update_query = "UPDATE Customer SET "
            update_values = []

            for column, value in columns_and_values.items():
                if value is not None:
                    update_query += f"{column} = %s, "
                    update_values.append(value)

            update_query = update_query.rstrip(', ')
            update_query += " WHERE customer_SSN_SIN = %s"
            update_values.append(customer_SSN_SIN)

            self.cursor.execute(update_query, tuple(update_values))
            self.commit()

        except Exception as e:
            self.connection.rollback()
            return (False, f"Error updating customer: {e}")

        return (True, "Customer information successfully updated")

    def delete_customer(self, ssn_sin): 
        self.cursor.execute("DELETE FROM Customer WHERE customer_SSN_SIN = %s", (ssn_sin,))
        self.cursor.execute("DELETE FROM Users WHERE user_SSN_SIN = %s", (ssn_sin,))
        self.commit()

    def delete_employee(self, ssn_sin): 
        self.cursor.execute("DELETE FROM Employee WHERE employee_SSN_SIN = %s", (ssn_sin,))
        self.cursor.execute("DELETE FROM Users WHERE user_SSN_SIN = %s", (ssn_sin,))
        self.commit()
    
    def delete_hotel_chain(self, chain_id):
        self.cursor.execute("DELETE FROM Hotel_Chain WHERE chain_ID = %s", (chain_id,))
        self.commit()
    
    def delete_hotel(self, hotel_id):
        self.cursor.execute("DELETE FROM Hotel WHERE hotel_ID = %s", (hotel_id,))
        self.commit()
    
    def delete_room(self, room_number, hotel_id):
        self.cursor.execute("DELETE FROM Room WHERE room_number = %s AND hotel_ID = %s", (room_number, hotel_id))
        self.commit()
    
    def cancel_booking(self, booking_id):
        try:
            self.cursor.execute(
                "UPDATE Booking SET canceled = TRUE WHERE booking_ID = %s",
                (booking_id,)
            )
            self.connection.commit()

            # Check if any rows were affected (i.e., the booking was found and updated)
            if self.cursor.rowcount > 0:
                return True, "Booking successfully canceled."
            else:
                return False, "Booking not found."
        except Exception as e:
            self.connection.rollback()
            return False, f"Error: {str(e)}"

    def get_rooms_per_area_by_date(self, start_date, end_date):

        view_definition_string = """
        CREATE OR REPLACE VIEW available_rooms_in_area AS
        SELECT address_country, address_province_state, address_city, COUNT(*)
        FROM Room NATURAL JOIN Hotel
        WHERE (room_number, hotel_ID) NOT IN (
            (
                SELECT room_number, hotel_ID
                FROM rental
                WHERE check_in_date > %s AND check_out_date < %s
            )
            UNION
            (
                SELECT room_number, hotel_ID
                FROM booking
                WHERE scheduled_check_in_date > %s AND scheduled_check_out_date < %s AND canceled = false
            )
        )
        GROUP BY address_country, address_province_state, address_city;

        SELECT * FROM available_rooms_in_area;
        """

        self.cursor.execute(view_definition_string, (start_date, end_date, start_date, end_date,))
        results = self.cursor.fetchall()
        return results
    
    def get_rooms_capacity(self):

        query = """
        SELECT hotel_chain_name, chain_id, hotel_id, room_number, room_capacity
        FROM hotel_total_room_capacity;
        """

        self.cursor.execute(query)
        results = self.cursor.fetchall()

        return results


    def get_rooms_capacity_by_hotel(self, hotel_id):

        query = """
        SELECT hotel_chain_name, chain_id, hotel_id, room_number, room_capacity
        FROM hotel_total_room_capacity WHERE hotel_id = %s;
        """

        self.cursor.execute(query, (hotel_id,))
        results = self.cursor.fetchall()

        return results

#db = Database(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
if __name__ == '__main__':
    test_db = Database(TEST_DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    '''
    start_date = '2023-04-07'
    end_date = '2023-04-13'
    res = test_db.search_hotels_and_rooms(start_date, end_date)
    # to print out the results of the search query properly.
    for chain in res:
        print(f"Chain Name: {chain['chain_name']}")
        for hotel in chain['hotels']:
            print(f"\tHotel Name: {hotel['address_street_name']}")
            print(f"\tAddress: {hotel['address_street_number']} {hotel['address_street_name']}, {hotel['address_city']}, {hotel['address_province_state']}, {hotel['address_country']}")
            print(f"\tContact Email: {hotel['contact_email']}")
            print(f"\tStar Rating: {hotel['star_rating']}")
            for room in hotel['rooms']:
                print(f"\t\tRoom Number: {room['room_number']}")
                print(f"\t\tRoom Capacity: {room['room_capacity']}")
                print(f"\t\tView Type: {room['view_type']}")
                print(f"\t\tPrice per Night: {room['price_per_night']}")
                print(f"\t\tIs Extendable: {room['is_extendable']}")
                print(f"\t\tRoom Problems: {room['room_problems']}")'''