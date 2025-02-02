import unittest
from flask import current_app
from flask_testing import TestCase
from main import create_app
from db.db_drivers import Database
from config import TestConfig
from flask_jwt_extended import decode_token, get_jwt
import json

app_instance = None

class TestAuth(TestCase):

    def create_app(self):
        # Access the global app_instance variable.
        global app_instance

        # If the app_instance is None, call the create_app function and store the result in app_instance.
        if app_instance is None:
            app_instance = create_app(TestConfig)
            app_instance.db.insert_test_data()

        # Return the app_instance.
        return app_instance

    def test_customer_registration(self):
        # Test data
        ssn_sin = 123456789
        first_name = "John"
        last_name = "Doe"
        password = "password123"
        address_street_name = "Test Street"
        address_street_number = 123
        address_city = "Test City"
        address_province_state = "Test State"
        address_country = "Test Country"

        # Make a request to the /auth/customers endpoint
        response = self.client.post("/auth/customers", json={
            "customer_SSN_SIN": ssn_sin,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "address_street_name": address_street_name,
            "address_street_number": address_street_number,
            "address_city": address_city,
            "address_province_state": address_province_state,
            "address_country": address_country,
        })

        with current_app.app_context():
            current_app.db.delete_customer(ssn_sin)

        # Check if the response is successful
        self.assertEqual(response.status_code, 200, f"Failed to register customer: {response.data}")

        # Check if the response contains the expected message
        self.assertEqual(response.json["message"], "Customer successfully registered.")
    
    def test_employee_registration(self):
        # Test data
        ssn_sin = 123456780
        employee_id = 1
        first_name = "John"
        last_name = "Doe"
        password = "password123"
        address_street_name = "Test Street"
        address_street_number = 123
        address_city = "Test City"
        address_province_state = "Test State"
        address_country = "Test Country"
        hotel_id = 1
        is_manager = False
        role = "Receptionist"

        # Make a request to the /auth/employees endpoint
        response = self.client.post("/auth/employees", json={
            "employee_SSN_SIN": ssn_sin,
            "employee_ID": employee_id,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "address_street_name": address_street_name,
            "address_street_number": address_street_number,
            "address_city": address_city,
            "address_province_state": address_province_state,
            "address_country": address_country,
            "hotel_ID": hotel_id,
            "is_manager": is_manager,
            "role": role
        })

        with current_app.app_context():
           current_app.db.delete_employee(ssn_sin)

        # Check if the response is successful
        self.assertEqual(response.status_code, 200, f"Failed to register employee: {response.data}")

        # Check if the response contains the expected message
        self.assertEqual(response.json["message"], "Employee registered successfully.")
    
    def test_customer_registration_conflict(self):
        # Test data
        ssn_sin = 123456789
        first_name = "John"
        last_name = "Doe"
        password = "password123"
        address_street_name = "Test Street"
        address_street_number = 123
        address_city = "Test City"
        address_province_state = "Test State"
        address_country = "Test Country"

        # First registration attempt
        response1 = self.client.post("/auth/customers", json={
            "customer_SSN_SIN": ssn_sin,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "address_street_name": address_street_name,
            "address_street_number": address_street_number,
            "address_city": address_city,
            "address_province_state": address_province_state,
            "address_country": address_country,
        })

        # Second registration attempt with the same SSN_SIN
        response2 = self.client.post("/auth/customers", json={
            "customer_SSN_SIN": ssn_sin,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "address_street_name": address_street_name,
            "address_street_number": address_street_number,
            "address_city": address_city,
            "address_province_state": address_province_state,
            "address_country": address_country,
        })

        # Clean up the test user
        with current_app.app_context():
            current_app.db.delete_customer(ssn_sin)

        # Check if the first response is successful
        self.assertEqual(response1.status_code, 200, f"Failed to register customer: {response1.data}")

        # Check if the second response returns a conflict error
        self.assertEqual(response2.status_code, 409, f"Second registration attempt did not return a conflict error: {response2.data}")

        # Check if the response contains the expected message
        self.assertEqual(response2.json["message"], "Error: Customer or Employee with the same SSN/SIN already exists.")
    

    def test_login(self):
        # Test data
        user_ssn_sin = 223456789
        first_name = "John"
        last_name = "Doe"
        password = "password123"
        address_street_name = "Test Street"
        address_street_number = 123
        address_city = "Test City"
        address_province_state = "Test State"
        address_country = "Test Country"
        role = "customer"

        # Register the user
        registration_response = self.client.post("/auth/customers", json={
            "customer_SSN_SIN": user_ssn_sin,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "address_street_name": address_street_name,
            "address_street_number": address_street_number,
            "address_city": address_city,
            "address_province_state": address_province_state,
            "address_country": address_country,
        })

        # Make a request to the /auth/login endpoint
        login_response = self.client.post("/auth/login", json={
            "user_SSN_SIN": str(user_ssn_sin),
            "password": password,
            "role": role
        })

        # Clean up the test user
        with current_app.app_context():
            current_app.db.delete_customer(user_ssn_sin)

        # Check if the registration response is successful
        self.assertEqual(registration_response.status_code, 200, f"Failed to register customer: {registration_response.data}")

        # Check if the login response is successful
        self.assertEqual(login_response.status_code, 200, f"Failed to log in user: {login_response.data}")

        # Check if the login response contains an access token
        self.assertIn("access_token", login_response.json, "Access token not found in the response")
    
    def test_login2(self):
        # Test data
        user_ssn_sin = 223456789
        first_name = "John"
        last_name = "Doe"
        password = "password123"
        address_street_name = "Test Street"
        address_street_number = 123
        address_city = "Test City"
        address_province_state = "Test State"
        address_country = "Test Country"
        role = "customer"

        # Register the user
        registration_response = self.client.post("/auth/customers", json={
            "customer_SSN_SIN": user_ssn_sin,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "address_street_name": address_street_name,
            "address_street_number": address_street_number,
            "address_city": address_city,
            "address_province_state": address_province_state,
            "address_country": address_country,
        })

        # Test login with correct credentials
        login_response = self.client.post("/auth/login", json={
            "user_SSN_SIN": str(user_ssn_sin),
            "password": password,
            "role": role
        })

        self.assertEqual(login_response.status_code, 200, f"Failed to log in user: {login_response.data}")
        self.assertIn("access_token", login_response.json, "Access token not found in the response")

        access_token = login_response.json["access_token"]

        # Test login with incorrect password
        login_response = self.client.post("/auth/login", json={
            "user_SSN_SIN": str(user_ssn_sin),
            "password": "wrong_password",
            "role": role
        })

        self.assertEqual(login_response.status_code, 401, f"User was able to log in with incorrect password: {login_response.data}")
        self.assertNotIn("access_token", login_response.json, "Access token found in the response")

        # Test login with non-existent user
        login_response = self.client.post("/auth/login", json={
            "user_SSN_SIN": "000000000",
            "password": "password",
            "role": role
        })

        self.assertEqual(login_response.status_code, 401, f"Non-existent user was able to log in: {login_response.data}")
        self.assertNotIn("access_token", login_response.json, "Access token found in the response")

        # Test login with incorrect role
        login_response = self.client.post("/auth/login", json={
            "user_SSN_SIN": str(user_ssn_sin),
            "password": password,
            "role": "wrong_role"
        })

        self.assertEqual(login_response.status_code, 401, f"User was able to log in with incorrect role: {login_response.data}")
        self.assertNotIn("access_token", login_response.json, "Access token found in the response")

        # Clean up the test user
        with current_app.app_context():
            current_app.db.delete_customer(user_ssn_sin)
    
    def test_employee_login_is_manager(self):
        # Test data
        employee_ssn_sin = 123453789
        employee_id = 1
        password = "password123"
        first_name = "John"
        last_name = "Doe"
        address_street_name = "Arrow Street"
        address_street_number = 123
        address_city = "Test City"
        address_province_state = "Test State"
        address_country = "Test Country"
        hotel_id = 1
        is_manager = True

        # Register the employee
        registration_response = self.client.post("/auth/employees", json={
            "employee_SSN_SIN": employee_ssn_sin,
            "employee_ID": employee_id,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "address_street_name": address_street_name,
            "address_street_number": address_street_number,
            "address_city": address_city,
            "address_province_state": address_province_state,
            "address_country": address_country,
            "hotel_ID": hotel_id,
            "is_manager": is_manager,
            "role": "employee"
        })

        # Make a request to the /auth/login endpoint
        login_response = self.client.post("/auth/login", json={
            "user_SSN_SIN": employee_ssn_sin,
            "password": password,
            "role": "employee"
        })

        # Clean up the test employee
        with current_app.app_context():
           current_app.db.delete_employee(employee_ssn_sin)

        # Check if the registration response is successful
        self.assertEqual(registration_response.status_code, 200, f"Failed to register employee: {registration_response.data}")

        # Check if the login response is successful
        self.assertEqual(login_response.status_code, 200, f"Failed to log in user: {login_response.data}")

        # Check if the login response contains an access token
        self.assertIn("access_token", login_response.json, "Access token not found in the response")

        # Check if the is_manager value is True in the access token
        access_token = login_response.json["access_token"]
        token_data = decode_token(access_token)
        self.assertEqual(token_data["is_manager"], True, "is_manager value is not True in the access token")
    
    def test_hotel_chains(self):
        with current_app.app_context():

            employee_ssn_sin = 123453789
            employee_id = 1
            password = "password123"
            first_name = "John"
            last_name = "Doe"
            address_street_name = "Arrow Street"
            address_street_number = 123
            address_city = "Test City"
            address_province_state = "Test State"
            address_country = "Test Country"
            hotel_id = 1
            is_manager = True

            # Register the employee
            registration_response = self.client.post("/auth/employees", json={
                "employee_SSN_SIN": employee_ssn_sin,
                "employee_ID": employee_id,
                "first_name": first_name,
                "last_name": last_name,
                "password": password,
                "address_street_name": address_street_name,
                "address_street_number": address_street_number,
                "address_city": address_city,
                "address_province_state": address_province_state,
                "address_country": address_country,
                "hotel_ID": hotel_id,
                "is_manager": is_manager,
                "role": "employee"
            })

            # Make a request to the /auth/login endpoint
            login_response = self.client.post("/auth/login", json={
                "user_SSN_SIN": employee_ssn_sin,
                "password": password,
                "role": "employee"
            })

            jwt_token = json.loads(login_response.data.decode())['access_token']

            # Make a request to add a hotel chain with the manager's JWT token
            response = self.client.post("/hotel_chain/hotel_chain", json={
                "chain_ID": 3,
                "name": "Hotel Chain 3",
                "number_of_hotels": 5
            }, headers={'Authorization': f'Bearer {jwt_token}'})

            # Check if the response is successful
            self.assertEqual(response.status_code, 201, f"Failed to add hotel chain: {response.data}")

            # Check if the response contains the expected message
            self.assertEqual(response.json["message"], "Hotel chain added successfully.", "Unexpected message")

            response = self.client.put("/hotel_chain/hotel_chain", json={
                "chain_ID": 3,
                "name": "New Hotel Chain 3",
                "number_of_hotels": 6
            }, headers={"Authorization": f"Bearer {jwt_token}"})
            self.assertEqual(response.status_code, 200, f"Failed to update hotel chain: {response.data}")
            self.assertEqual(response.json["message"], "Hotel chain updated successfully.", "Unexpected message")
            hotel_chain = current_app.db.get_hotel_chain(3)
            self.assertIsNotNone(hotel_chain, "Hotel chain not found in the database")
            self.assertEqual(hotel_chain[0][1], "New Hotel Chain 3", "Incorrect hotel chain name")
            self.assertEqual(hotel_chain[0][2], 6, "Incorrect number of hotels")

            # Delete the hotel chain using the manager's JWT
            response = self.client.delete("/hotel_chain/hotel_chain/3", headers={"Authorization": f"Bearer {jwt_token}"})
            self.assertEqual(response.status_code, 200, f"Failed to delete hotel chain: {response.data}")

            # Confirm that the hotel chain was deleted
            response = self.client.get("/hotel_chain/hotel_chain/3")
            self.assertEqual(response.status_code, 404, "Hotel chain still exists in the database")

            # Check if the hotel chain was added to the database
            with current_app.app_context():

                # Clean up the test data
                current_app.db.delete_employee(employee_ssn_sin)
    
    def get_manager_token(self):
        # Test data
        employee_ssn_sin = 123453789
        employee_id = 1
        password = "password123"
        first_name = "John"
        last_name = "Doe"
        address_street_name = "Arrow Street"
        address_street_number = 123
        address_city = "Test City"
        address_province_state = "Test State"
        address_country = "Test Country"
        hotel_id = 1
        is_manager = True

        # Register the employee
        registration_response = self.client.post("/auth/employees", json={
            "employee_SSN_SIN": employee_ssn_sin,
            "employee_ID": employee_id,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "address_street_name": address_street_name,
            "address_street_number": address_street_number,
            "address_city": address_city,
            "address_province_state": address_province_state,
            "address_country": address_country,
            "hotel_ID": hotel_id,
            "is_manager": is_manager,
            "role": "employee"
        })

        # Make a request to the /auth/login endpoint
        login_response = self.client.post("/auth/login", json={
            "user_SSN_SIN": employee_ssn_sin,
            "password": password,
            "role": "employee"
        })

        jwt_token = json.loads(login_response.data.decode())['access_token']

        with current_app.app_context():
            current_app.db.delete_employee(employee_ssn_sin)
            current_app.db.delete_hotel(1)

        return jwt_token

    def test_insert_update_delete_hotel(self):
        jwt_token = self.get_manager_token()

        # Insert hotel
        response = self.client.post("/hotel/hotel", json={
            "hotel_ID": 1,
            "chain_ID": 1,
            "number_of_rooms": 100,
            "address_street_name": "Test Street",
            "address_street_number": 123,
            "address_city": "Test City",
            "address_province_state": "Test State",
            "address_country": "Test Country",
            "contact_email": "test@email.com",
            "star_rating": 4
        }, headers={'Authorization': f'Bearer {jwt_token}'})

        self.assertEqual(response.status_code, 201, f"Failed to insert hotel: {response.data}")
        self.assertEqual(response.json["message"], "Hotel added successfully.", "Unexpected message")

        # Update hotel
        response = self.client.put("/hotel/hotel", json={
            "hotel_ID": 1,
            "chain_ID": 1,
            "number_of_rooms": 200,
            "address_street_name": "Updated Test Street",
            "address_street_number": 321,
            "address_city": "Updated Test City",
            "address_province_state": "Updated Test State",
            "address_country": "Updated Test Country",
            "contact_email": "updated_test@email.com",
        }, headers={'Authorization': f'Bearer {jwt_token}'})

        self.assertEqual(response.status_code, 200, f"Failed to update hotel: {response.data}")
        self.assertEqual(response.json["message"], "Hotel updated successfully.", "Unexpected message")

        # Get updated hotel
        response = self.client.get("/hotel/hotel/1")
        self.assertEqual(response.status_code, 200, f"Failed to get updated hotel: {response.data}")

        updated_hotel = response.json
        self.assertEqual(updated_hotel["address_street_name"], "Updated Test Street", "Unexpected address street name")
        self.assertEqual(updated_hotel["address_street_number"], 321, "Unexpected address street number")
        self.assertEqual(updated_hotel["address_city"], "Updated Test City", "Unexpected address city")
        self.assertEqual(updated_hotel["address_province_state"], "Updated Test State", "Unexpected address province state")
        self.assertEqual(updated_hotel["address_country"], "Updated Test Country", "Unexpected address country")
        self.assertEqual(updated_hotel["contact_email"], "updated_test@email.com", "Unexpected email")
        self.assertEqual(updated_hotel["number_of_rooms"], 200, "Unexpected number of rooms")

        # Delete hotel
        # response = self.client.delete("/hotel/hotel/1", headers={'Authorization': f'Bearer {jwt_token}'})
        # self.assertEqual(response.status_code, 200, f"Failed to delete hotel: {response.data}")
        # self.assertEqual(response.json["message"], "Hotel removed successfully.", "Unexpected message")

    
    def test_update_customer_successful(self):
        # Test data
        ssn_sin = 123456789
        first_name = "John"
        last_name = "Doe"
        password = "password123"
        address_street_name = "Test Street"
        address_street_number = 123
        address_city = "Test City"
        address_province_state = "Test State"
        address_country = "Test Country"
        role = "customer"

        # Register the customer
        registration_response = self.client.post("/auth/customers", json={
            "customer_SSN_SIN": ssn_sin,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "address_street_name": address_street_name,
            "address_street_number": address_street_number,
            "address_city": address_city,
            "address_province_state": address_province_state,
            "address_country": address_country,
        })

        # Login as the customer
        login_response = self.client.post("/auth/login", json={
            "user_SSN_SIN": ssn_sin,
            "password": password,
            "role": role
        })

        print(login_response.json)
        access_token = login_response.json["access_token"]
        headers = {'Authorization': f'Bearer {access_token}'}

        # Update the customer's information
        update_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "address_street_name": "New Street",
            "address_street_number": 456,
            "address_city": "New City",
            "address_province_state": "New State",
            "address_country": "New Country"
        }

        update_response = self.client.put(f"/auth/customers/{ssn_sin}", headers=headers, json=update_data)

        # Check if the registration response is successful
        self.assertEqual(registration_response.status_code, 200, f"Failed to register customer: {registration_response.data}")

        # Check if the login response is successful
        self.assertEqual(login_response.status_code, 200, f"Failed to log in user: {login_response.data}")

        # Check if the update response is successful
        self.assertEqual(update_response.status_code, 200, f"Failed to update customer information: {update_response.data}")

        # Check if the customer's data was updated in the database
        customer_response = self.client.get(f"/auth/customers/{ssn_sin}", headers=headers)
        customer_data = customer_response.json
        print(customer_data)

        # Check if the customer's data was updated
        self.assertEqual(customer_data["first_name"], "Jane", "Unexpected first name update")
        self.assertEqual(customer_data["last_name"], "Doe", "Unexpected last name update")
        self.assertEqual(customer_data["address_street_name"], "New Street", "Unexpected street name update")
        self.assertEqual(customer_data["address_street_number"], 456, "Unexpected street number update")
        self.assertEqual(customer_data["address_city"], "New City", "Unexpected city update")
        self.assertEqual(customer_data["address_province_state"], "New State", "Unexpected province/state update")
        self.assertEqual(customer_data["address_country"], "New Country", "Unexpected country update")
        
        # Clean up the test customer
        with current_app.app_context():
            current_app.db.delete_customer(ssn_sin)

    def test_customer_details(self):
        # Test data
        customer_ssn_sin = 123456789
        wrong_customer_ssn_sin = 123456788
        customer_password = "password123"
        first_name = "John"
        last_name = "Doe"
        address_street_name = "Test Street"
        address_street_number = 123
        address_city = "Test City"
        address_province_state = "Test State"
        address_country = "Test Country"

        # Register the customer
        registration_response = self.client.post("/auth/customers", json={
            "customer_SSN_SIN": customer_ssn_sin,
            "first_name": first_name,
            "last_name": last_name,
            "password": customer_password,
            "address_street_name": address_street_name,
            "address_street_number": address_street_number,
            "address_city": address_city,
            "address_province_state": address_province_state,
            "address_country": address_country,
        })
        print("registratin was fine")

        # Test that a customer can see their own information
        customer_login_response = self.client.post("/auth/login", json={
            "user_SSN_SIN": customer_ssn_sin,
            "password": customer_password,
            "role": "customer"
        })
        print("login was fine")

        customer_access_token = customer_login_response.json["access_token"]
        headers = {"Authorization": f"Bearer {customer_access_token}"}
        customer_details_response = self.client.get(f"/auth/customers/{customer_ssn_sin}", headers=headers)
        self.assertEqual(customer_details_response.status_code, 200, f"Failed to get customer details: {customer_details_response.data}")

        # Test that a customer cannot see someone else's information
        headers = {"Authorization": f"Bearer {customer_access_token}"}
        customer_details_response = self.client.get(f"/auth/customers/{wrong_customer_ssn_sin}", headers=headers)
        self.assertEqual(customer_details_response.status_code, 401, f"Customer was able to access someone else's information: {customer_details_response.data}")

        # Clean up the test data
        with current_app.app_context():
            current_app.db.delete_customer(customer_ssn_sin)

    def test_update_employee_successful(self):
        with current_app.app_context():
            # Test data
            manager_SSN_SIN = 123453789
            manager_ID = 1
            manager_password = "manager_password123"
            first_name = "Manager"
            last_name = "Doe"
            address_street_name = "Test Street"
            address_street_number = 123
            address_city = "Test City"
            address_province_state = "Test State"
            address_country = "Test Country"
            role = "employee"
            hotel_ID = 1
            is_manager = True

            # Create a manager
            registration_response = self.client.post("/auth/employees", json={
                "employee_SSN_SIN": manager_SSN_SIN,
                "employee_ID": manager_ID,
                "first_name": first_name,
                "last_name": last_name,
                "password": manager_password,
                "address_street_name": address_street_name,
                "address_street_number": address_street_number,
                "address_city": address_city,
                "address_province_state": address_province_state,
                "address_country": address_country,
                "hotel_ID": hotel_ID,
                "is_manager": is_manager,
                "role": "employee"
            })

            # Login as manager
            login_response = self.client.post("/auth/login", json={
                "user_SSN_SIN": manager_SSN_SIN,
                "password": manager_password,
                "role": "employee"
            })
            jwt_token = login_response.json["access_token"]

            # Test data for employee
            employee_SSN_SIN = 123456789
            employee_ID = 987654321
            first_name = "John"
            last_name = "Doe"
            password = "password123"
            address_street_name = "Test Street"
            address_street_number = 123
            address_city = "Test City"
            address_province_state = "Test State"
            address_country = "Test Country"
            role = "employee"
            hotel_ID = 1
            is_manager = False

            # Register the employee
            registration_response = self.client.post("/auth/employees", json={
                "employee_SSN_SIN": employee_SSN_SIN,
                "employee_ID": employee_ID,
                "first_name": first_name,
                "last_name": last_name,
                "password": password,
                "address_street_name": address_street_name,
                "address_street_number": address_street_number,
                "address_city": address_city,
                "address_province_state": address_province_state,
                "address_country": address_country,
                "hotel_ID": hotel_ID,
                "is_manager": is_manager,
                "role": "employee"
            })

            # Login as the employee
            login_response = self.client.post("/auth/login", json={
                "user_SSN_SIN": employee_SSN_SIN,
                "password": password,
                "role": "employee"
            })

            access_token = login_response.json["access_token"]
            headers = {'Authorization': f'Bearer {access_token}'}

            # Update the employee's information
            update_data = {
                "first_name": "Jane",
                "last_name": "Doe",
                "address_street_name": "New Street",
                "address_street_number": 456,
                "address_city": "New City",
                "address_province_state": "New State",
                "address_country": "New Country"
            }

            update_response = self.client.put(f"/auth/employees/{employee_SSN_SIN}", headers=headers, json=update_data)

            # Check if the registration response is successful
            self.assertEqual(registration_response.status_code, 200, f"Failed to register employee: {registration_response.data}")

            # Check if the login response is successful
            self.assertEqual(login_response.status_code, 200, f"Failed to log in user: {login_response.data}")

            # Check if the update response is successful
            self.assertEqual(update_response.status_code, 200, f"Failed to update employee information: {update_response.data}")

            # Check if the employee's data was updated in the database
            employee_response = self.client.get(f"/auth/employees/{employee_SSN_SIN}", headers=headers)
            employee_data = employee_response.json

            # Check if the employee's data was updated
            self.assertEqual(employee_data["first_name"], "Jane", "Unexpected first name update")
            self.assertEqual(employee_data["last_name"], "Doe", "Unexpected last name update")
            self.assertEqual(employee_data["address_street_name"], "New Street", "Unexpected street name update")
            self.assertEqual(employee_data["address_street_number"], 456, "Unexpected street number update")
            self.assertEqual(employee_data["address_city"], "New City", "Unexpected city update")
            self.assertEqual(employee_data["address_province_state"], "New State", "Unexpected province/state update")
            self.assertEqual(employee_data["address_country"], "New Country", "Unexpected country update")

            # Clean up the test data
            with current_app.app_context():
                current_app.db.delete_employee(employee_SSN_SIN)
                current_app.db.delete_employee(manager_SSN_SIN)


    def test_insert_update_delete_room(self):
        # Register an employee with manager role and get their JWT token
        jwt_token = self.get_manager_token()

        # Insert a hotel chain and hotel
        self.client.post("/hotel_chain/hotel_chain", json={
            "chain_ID": 1,
            "name": "Hotel Chain 1",
            "number_of_hotels": 1
        }, headers={"Authorization": f"Bearer {jwt_token}"})

        self.client.post("/hotel/hotel", json={
            "hotel_ID": 1,
            "chain_ID": 1,
            "number_of_rooms": 100,
            "address_street_name": "Test Street",
            "address_street_number": 123,
            "address_city": "Test City",
            "address_province_state": "Test State",
            "address_country": "Test Country",
            "contact_email": "test@example.com",
            "star_rating": 4
        }, headers={"Authorization": f"Bearer {jwt_token}"})

        # Insert a new room
        response = self.client.post("/room/room", json={
            "room_number": 1,
            "hotel_ID": 1,
            "room_capacity": 2,
            "view_type": "ocean",
            "price_per_night": 100,
            "is_extendable": True,
            "room_problems": "None"
        }, headers={"Authorization": f"Bearer {jwt_token}"})

        self.assertEqual(response.status_code, 201, f"Failed to insert room: {response.data}")
        self.assertEqual(response.json["message"], "Room added successfully.", "Unexpected message")

        # Update the room
        response = self.client.put("/room/room", json={
            "room_number": 1,
            "hotel_ID": 1,
            "room_capacity": 4,
            "view_type": "ocean",
            "price_per_night": 200,
            "is_extendable": False,
            "room_problems": "None"
        }, headers={"Authorization": f"Bearer {jwt_token}"})

        self.assertEqual(response.status_code, 200, f"Failed to update room: {response.data}")
        self.assertEqual(response.json["message"], "Room updated successfully.", "Unexpected message")

        # Get the updated room
        response = self.client.get("/room/room/1/1")
        self.assertEqual(response.status_code, 200, f"Failed to get updated room: {response.data}")

        updated_room = response.json
        self.assertEqual(updated_room["room_capacity"], 4, "Unexpected room capacity")
        self.assertEqual(updated_room["price_per_night"], 200, "Unexpected price per night")
        self.assertEqual(updated_room["is_extendable"], False, "Unexpected value for is_extendable")

        # Delete the room
        response = self.client.delete("/room/room/1/1", headers={"Authorization": f"Bearer {jwt_token}"})
        self.assertEqual(response.status_code, 200, f"Failed to delete room: {response.data}")
        self.assertEqual(response.json["message"], "Room removed successfully.", "Unexpected message")

        # Delete the hotel and hotel chain
        # self.client.delete("/hotel/hotel/1", headers={"Authorization": f"Bearer {jwt_token}"})
        # self.client.delete("/hotel_chain/hotel_chain/1", headers={"Authorization": f"Bearer {jwt_token}"})
    

if __name__ == "__main__":
    unittest.main()
