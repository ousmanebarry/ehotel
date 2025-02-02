import os
import datetime
from dotenv import load_dotenv
from db_drivers import Database
import json
load_dotenv()

### TESTING THE DB DRIVERS ###  
def test_insert_hotel_chain(db):
    print("Inserting new hotel chain...")
    db.insert_hotel_chain(1, "Luxury Hotels", 10)
    print("Inserted hotel chain with chain_ID 1.")

    print("Updating hotel chain...")
    db.insert_hotel_chain(1, "Luxury Hotels International", 11)
    print("Updated hotel chain with chain_ID 1.")

    print("Printing all hotel chains...")
    hotel_chains = db.get_all_hotel_chains()
    assert len(hotel_chains) == 1
    assert hotel_chains[0][0] == 1
    assert hotel_chains[0][1] == "Luxury Hotels International"
    assert hotel_chains[0][2] == 11
    print("test 1 passed")

def test_insert_hotel(db):
    print("Inserting new hotel...")
    db.insert_hotel(1, 1, 100, "Sunset Boulevard", 123, "Los Angeles", "California", "USA", "contact@luxuryhotels.com", 5)
    print("Inserted hotel with hotel_ID 1.")

    print("Updating hotel...")
    db.insert_hotel(1, 1, 110, "Sunset Boulevard", 123, "Los Angeles", "California", "USA", "contact@luxuryhotels.com", 5)
    print("Updated hotel with hotel_ID 1.")

    print("Printing all hotels...")
    hotels = db.get_all_hotels()
    assert len(hotels) == 1
    assert hotels[0][0] == 1
    assert hotels[0][1] == 1
    assert hotels[0][2] == 110
    assert hotels[0][3] == "Sunset Boulevard"
    assert hotels[0][4] == 123
    assert hotels[0][5] == "Los Angeles"
    assert hotels[0][6] == "California"
    assert hotels[0][7] == "USA"
    assert hotels[0][8] == "contact@luxuryhotels.com"
    assert hotels[0][9] == 5
    print("test 2 passed")

def test_insert_customer(db):
    print("Inserting new customer...")
    db.insert_customer(123456789, "password", "John", "Doe", "123 Main St", 1, "Anytown", "ON", "Canada", "2022-01-01")
    print("Inserted customer with SSN/SIN 123456789.")

    print("Attempting to insert duplicate customer...")
    db.insert_customer(123456789, "new_password", "Jane", "Doe", "456 Main St", 2, "Othertown", "ON", "Canada", "2022-02-01")

    print("Printing all customers...")
    customers = db.get_all_customers()
    print(customers)
    assert len(customers) == 1
    assert customers[0][0] == 123456789
    assert customers[0][1] == "John"
    assert customers[0][2] == "Doe"
    assert customers[0][3] == "123 Main St"
    assert customers[0][4] == 1
    assert customers[0][5] == "Anytown"
    assert customers[0][6] == "ON"
    assert customers[0][7] == "Canada"
    assert customers[0][8] == datetime.date(2022, 1, 1)
    print("test_insert_customer passed")

def test_insert_employee(db):
    print("Inserting new employee...")
    db.insert_employee(987654321, 1, "password", "John", "Smith", "123 Main St", 1, "Anytown", "ON", "Canada", 1, True)
    print("Inserted employee with SSN/SIN 987654321 and employee ID 1.")

    print("Attempting to insert duplicate employee...")
    db.insert_employee(987654321, 1, "new_password", "Jane", "Smith", "456 Main St", 2, "Othertown", "ON", "Canada", 2, False)

    print("Printing all employees...")
    employees = db.get_all_employees()
    print(employees)
    assert len(employees) == 1
    assert employees[0][0] == 987654321
    assert employees[0][1] == 1
    assert employees[0][2] == "John"
    assert employees[0][3] == "Smith"
    assert employees[0][4] == "123 Main St"
    assert employees[0][5] == 1
    assert employees[0][6] == "Anytown"
    assert employees[0][7] == "ON"
    assert employees[0][8] == "Canada"
    assert employees[0][9] == 1
    assert employees[0][10] == True
    print("test_insert_employee passed")

def test_check_account_and_role(db):
    print("Testing check_account_and_role...")

    # Test case 1: Valid customer credentials
    result = db.check_account_and_role(123456789, "password", "customer")
    assert result[0] == "Found User"
    assert result[1] == "customer"
    print("Test case 1 passed")

    # Test case 2: Invalid customer password
    assert db.check_account_and_role(123456789, "wrong_password", "customer") == ["Invalid Password"]
    print("Test case 2 passed")

    # Test case 3: Valid employee credentials
    result = db.check_account_and_role(987654321, "password", "employee")
    assert result[0] == "Found User"
    assert result[1] == "employee"
    print("Test case 3 passed")

    # Test case 4: Invalid employee password
    assert db.check_account_and_role(987654321, "wrong_password", "employee") == ["Invalid Password"]
    print("Test case 4 passed")

    # Test case 5: Non-existent user SSN/SIN
    assert db.check_account_and_role(111111111, "password", "customer") == ["Invalid SSN/SIN"]
    print("Test case 5 passed")

    # Test case 6: Incorrect role for user
    assert db.check_account_and_role(123456789, "password", "employee") == ["Invalid Role"]
    print("Test case 6 passed")

    print("All test cases for check_account_and_role passed")

def test_insert_employee_role(db):
    print("Inserting new employee role...")
    db.insert_employee_role(987654321, 1, "Receptionist")
    print("Inserted employee role Receptionist for employee ID 1.")

    print("Inserting new employee role...")
    db.insert_employee_role(987654321, 1, "Manager")
    print("Inserted employee role Manager for employee ID 1.")

    print("Inserting new employee role...")
    db.insert_employee_role(987654321, 1, "Housekeeping")
    print("Inserted employee role Housekeeping for employee ID 1.")

    print("Inserting duplicate employee role...")
    db.insert_employee_role(987654321, 1, "Receptionist")
    print("Attempting to insert duplicate employee role Receptionist for employee ID 1.")

    print("Printing all employee roles...")
    employee_roles = db.get_employee_roles(987654321, 1)
    print(employee_roles)
    assert len(employee_roles) == 3
    assert "receptionist" in employee_roles
    assert "housekeeping" in employee_roles
    assert employee_roles.count("receptionist") == 1
    assert 'manager' == employee_roles[0]
    print("test_insert_employee_role passed")

def test_insert_room(db):
    print("Inserting new room...")
    db.insert_room(101, 1, 2, "Ocean", 250, True, "None")
    print("Inserted room with room_number 101.")

    print("Updating room...")
    db.insert_room(101, 1, 3, "Ocean", 300, True, "None")
    print("Updated room with room_number 101.")

    print("Printing all rooms...")
    rooms = db.get_all_rooms()
    assert len(rooms) == 1
    assert rooms[0][0] == 101
    assert rooms[0][1] == 1
    assert rooms[0][2] == 3
    assert rooms[0][3] == "Ocean"
    assert rooms[0][4] == 300
    assert rooms[0][5] == True
    assert rooms[0][6] == "None"
    print("test_insert_room passed")

def test_insert_booking(db):
    print("Inserting new booking...")
    db.insert_booking(1, 123456789, 101, 1, datetime.date(2023, 4, 10), datetime.date(2023, 4, 14))
    print("Inserted booking with customer SSN/SIN 123456789 and room number 101.")

    print("Attempting to insert duplicate booking...")
    db.insert_booking(1, 123456789, 101, 1, datetime.date(2023, 4, 11), datetime.date(2023, 4, 13))

    print("Attempting to insert booking with invalid check-in and check-out dates...")
    db.insert_booking(2, 123456789, 101, 1, datetime.date(2023, 4, 14), datetime.date(2023, 4, 10))

    print("Attempting to insert booking with same check-in and check-out date...")
    db.insert_booking(3, 123456789, 101, 1, datetime.date(2023, 4, 10), datetime.date(2023, 4, 10))

    print("Printing all bookings...")
    bookings = db.get_all_bookings()
    print(bookings)
    assert len(bookings) == 1
    assert bookings[0][0] == 1
    assert bookings[0][1] == datetime.date.today()
    assert bookings[0][2] == datetime.date(2023, 4, 10)
    assert bookings[0][3] == datetime.date(2023, 4, 14)
    assert bookings[0][4] == False
    assert bookings[0][5] == 123456789
    assert bookings[0][6] == 101
    assert bookings[0][7] == 1
    print("test_insert_booking passed")


def test_convert_booking_to_rental(db):
    print("Converting booking to rental")

    # Clear the tables
    db.clear_table("Rental")
    db.clear_table("Booking")
    db.clear_table("Customer")
    db.clear_table("Employee")
    db.clear_table("Users")

    # Add an employee
    employee_ssn_sin = 123456789
    employee_id = 1
    password = "password123"
    first_name = "John"
    last_name = "Doe"
    address_street_name = "Main St."
    address_street_number = "123"
    address_city = "New York"
    address_province_state = "NY"
    address_country = "USA"
    hotel_id = 1
    is_manager = True
    db.insert_employee(employee_ssn_sin, employee_id, password, first_name, last_name, address_street_name, address_street_number, address_city, address_province_state, address_country, hotel_id, is_manager)

    # Add a customer
    customer_ssn_sin = 987654321
    password = "password456"
    first_name = "Jane"
    last_name = "Doe"
    address_street_name = "Broadway"
    address_street_number = "456"
    address_city = "New York"
    address_province_state = "NY"
    address_country = "USA"
    registration_date = datetime.date.today()
    db.insert_customer(customer_ssn_sin, password, first_name, last_name, address_street_name, address_street_number, address_city, address_province_state, address_country, registration_date)

    # Add a booking
    booking_id = 1
    room_number = 101
    check_in_date = datetime.date(2023, 4, 10)
    check_out_date = datetime.date(2023, 4, 14)
    db.insert_booking(booking_id, customer_ssn_sin, room_number, hotel_id, check_in_date, check_out_date)
    print(db.get_all_bookings())

    # Convert booking to rental
    total_paid = 1200
    discount = 0
    additional_charges = 0
    db.convert_booking_to_rental(booking_id, total_paid, discount, additional_charges)

    # Retrieve the rental information
    rentals = db.get_all_rentals()
    assert len(rentals) == 1
    rental = rentals[0]
    print(rental)

    # Check if the booking has been successfully converted to a rental
    assert rental[0] == booking_id
    assert rental[3] == total_paid
    assert rental[4] == discount
    assert rental[5] == additional_charges
    assert rental[8] == customer_ssn_sin
    assert rental[10] == room_number
    assert rental[11] == hotel_id
    assert rental[6] == check_in_date
    assert rental[7] == check_out_date

    print("test_convert_booking_to_rental passed")

def test_create_rental(db):

    # Clear the tables
    db.clear_table("Rental")
    db.clear_table("Customer")
    db.clear_table("Employee")
    db.clear_table("Users")

    # Add an employee
    employee_ssn_sin = 123456789
    employee_id = 1
    password = "password123"
    first_name = "John"
    last_name = "Doe"
    address_street_name = "Main St."
    address_street_number = "123"
    address_city = "New York"
    address_province_state = "NY"
    address_country = "USA"
    hotel_id = 1
    is_manager = True
    db.insert_employee(employee_ssn_sin, employee_id, password, first_name, last_name, address_street_name, address_street_number, address_city, address_province_state, address_country, hotel_id, is_manager)

    # Add a customer
    customer_ssn_sin = 987654321
    password = "password456"
    first_name = "Jane"
    last_name = "Doe"
    address_street_name = "Broadway"
    address_street_number = "456"
    address_city = "New York"
    address_province_state = "NY"
    address_country = "USA"
    registration_date = datetime.date.today()
    db.insert_customer(customer_ssn_sin, password, first_name, last_name, address_street_name, address_street_number, address_city, address_province_state, address_country, registration_date)

    check_in_date = datetime.date.today() + datetime.timedelta(days=3)
    check_out_date = datetime.date.today() + datetime.timedelta(days=5)
    total_paid = 300
    discount = 0
    additional_charges = 0
    db.create_rental(101, hotel_id, customer_ssn_sin, check_in_date, check_out_date, total_paid, discount, additional_charges)

    # Retrieve the rental information
    rentals = db.get_all_rentals()
    print(rentals)
    assert len(rentals) == 1
    rental = rentals[0]
    print(rental[6])
    print(rental)

    # Check if the rental has been successfully created
    assert rental[3] == total_paid
    assert rental[4] == discount
    assert rental[5] == additional_charges
    assert rental[8] == customer_ssn_sin
    assert rental[10] == 101
    assert rental[11] == hotel_id
    assert rental[6] == check_in_date
    assert rental[7] == check_out_date

    print("test_create_rental passed")


def test_search_hotels_and_rooms(db):

    # Clear the tables
    db.clear_table("Rental")
    db.clear_table("Customer")
    db.clear_table("Employee")
    db.clear_table("Users")
    db.clear_table("Hotel_Chain")
    db.clear_table("Hotel")
    db.clear_table("Room")
    db.clear_table("Has_Amenity")

    # Create test data
    db.cursor.execute("INSERT INTO Hotel_Chain (chain_ID, name, number_of_hotels) VALUES (1, 'Hilton', 2)")
    db.cursor.execute("INSERT INTO Hotel_Chain (chain_ID, name, number_of_hotels) VALUES (2, 'Marriott', 1)")
    db.cursor.execute("INSERT INTO Hotel (hotel_ID, chain_ID, number_of_rooms, address_street_name, address_street_number, address_city, address_province_state, address_country, contact_email, star_rating) VALUES (1, 1, 100, 'Main St', 123, 'New York', 'NY', 'USA', 'hilton@hilton.com', 4)")
    db.cursor.execute("INSERT INTO Hotel (hotel_ID, chain_ID, number_of_rooms, address_street_name, address_street_number, address_city, address_province_state, address_country, contact_email, star_rating) VALUES (2, 1, 50, '2nd St', 456, 'New York', 'NY', 'USA', 'hilton@hilton.com', 5)")
    db.cursor.execute("INSERT INTO Hotel (hotel_ID, chain_ID, number_of_rooms, address_street_name, address_street_number, address_city, address_province_state, address_country, contact_email, star_rating) VALUES (3, 2, 200, '3rd St', 789, 'Chicago', 'IL', 'USA', 'marriott@marriott.com', 2)")
    db.cursor.execute("INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems) VALUES (101, 1, 2, 'city', 100, True, NULL)")
    db.cursor.execute("INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems) VALUES (102, 1, 2, 'city', 110, False, 'Noisy')")
    db.cursor.execute("INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems) VALUES (201, 2, 4, 'ocean', 200, True, NULL)")
    db.cursor.execute("INSERT INTO Room (room_number, hotel_ID, room_capacity, view_type, price_per_night, is_extendable, room_problems) VALUES (301, 3, 2, 'city', 150, True, NULL)")
    db.cursor.execute("INSERT INTO Has_Amenity (amenity_id, hotel_id, room_number) VALUES (1, 1, 101)")
    db.cursor.execute("INSERT INTO Has_Amenity (amenity_id, hotel_id, room_number) VALUES (2, 1, 102)")
    db.cursor.execute("INSERT INTO Has_Amenity (amenity_id, hotel_id, room_number) VALUES (1, 2, 201)")
    db.commit()

    # Test with view type and room capacity
    return db.search_hotels_and_rooms(star_rating=2)
    

def format_output(hotel_data):
    formatted_data = []
    for hotel in hotel_data:
        formatted_hotel = {
            'hotel_ID': hotel['hotel_ID'],
            'chain_ID': hotel['chain_ID'],
            'number_of_rooms': hotel['number_of_rooms'],
            'address_street_name': hotel['address_street_name'],
            'address_street_number': hotel['address_street_number'],
            'address_city': hotel['address_city'],
            'address_province_state': hotel['address_province_state'],
            'address_country': hotel['address_country'],
            'contact_email': hotel['contact_email'],
            'star_rating': hotel['star_rating'],
            'rooms': []
        }
        for room in hotel['rooms']:
            formatted_room = {
                'room_number': room['room_number'],
                'room_capacity': room['room_capacity'],
                'view_type': room['view_type'],
                'price_per_night': room['price_per_night'],
                'is_extendable': room['is_extendable'],
                'room_problems': room['room_problems']
            }
            formatted_hotel['rooms'].append(formatted_room)
        formatted_data.append(formatted_hotel)
    return formatted_data


if __name__ == "__main__":
    # Replace the following with your actual database connection details
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    TEST_DB_NAME = os.getenv('TEST_DB_NAME')

    # Create a Database instance and run the test functions
    test_db = Database(TEST_DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    test_db.cursor.execute("DROP TABLE IF EXISTS Hotel_Chain, Hotel, Employee, Employee_Role, Hotel_Phone_Number, Hotel_Chain_Central_Office_Address, Hotel_Chain_Contact_Email, Hotel_Chain_Phone_Number, Room, Amenity, Has_Amenity, Customer, Booking, Rental, Users CASCADE")
    test_db.cursor.execute("""
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
        FOREIGN KEY (hotel_ID) REFERENCES Hotel(hotel_ID)
        );

        CREATE TABLE Employee_Role (
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
        FOREIGN KEY (hotel_ID) REFERENCES Hotel(hotel_ID)
        );

        CREATE TABLE IF NOT EXISTS Hotel_Chain_Central_Office_Address (
        chain_ID INT,
        address_street_name VARCHAR(50) NOT NULL,
        address_street_number INT NOT NULL,
        address_city VARCHAR(50) NOT NULL,
        address_province_state VARCHAR(50) NOT NULL,
        address_country VARCHAR(50) NOT NULL,
        PRIMARY KEY (chain_ID),
        FOREIGN KEY (chain_ID) REFERENCES Hotel_Chain(chain_ID)
        );

        CREATE TABLE IF NOT EXISTS Hotel_Chain_Contact_Email (
        chain_ID INT,
        contact_email VARCHAR(50) NOT NULL,
        PRIMARY KEY (chain_ID),
        FOREIGN KEY (chain_ID) REFERENCES Hotel_Chain(chain_ID)
        );

        CREATE TABLE IF NOT EXISTS Hotel_Chain_Phone_Number (
        chain_ID INT,
        phone_number VARCHAR(12),
        PRIMARY KEY (chain_ID, phone_number),
        FOREIGN KEY (chain_ID) REFERENCES Hotel_Chain(chain_ID)
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
        amenity_name VARCHAR(50) NOT NULL,
        PRIMARY KEY (amenity_id)
        );

        CREATE TABLE IF NOT EXISTS Has_Amenity (
        amenity_id INT,
        hotel_id INT,
        room_number INT,
        PRIMARY KEY (amenity_id, hotel_id, room_number),
        FOREIGN KEY (hotel_id, room_number) REFERENCES Room(hotel_ID, room_number) ON DELETE CASCADE
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
            FOREIGN KEY (room_number, hotel_ID) REFERENCES Room(room_number, hotel_ID)
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
        FOREIGN KEY (room_number, hotel_ID) REFERENCES Room(room_number, hotel_ID)
        );

        CREATE TABLE IF NOT EXISTS Users (
            user_SSN_SIN INT PRIMARY KEY,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(10) NOT NULL,
            CHECK (role = 'customer' OR role = 'employee')
        );
        """)
    test_db.commit()

    test_insert_hotel_chain(test_db)
    test_insert_hotel(test_db)
    test_insert_customer(test_db)
    test_insert_employee(test_db)
    test_check_account_and_role(test_db)
    test_insert_employee_role(test_db)
    test_insert_room(test_db)
    test_insert_booking(test_db)
    test_convert_booking_to_rental(test_db)
    test_create_rental(test_db)
    print(test_search_hotels_and_rooms(test_db))
    print(json.dumps(test_search_hotels_and_rooms(test_db), indent=2))
    print("--------------------------------")
    print("ALL TESTS PASSED")

    # Close the database connection
    test_db.close()

