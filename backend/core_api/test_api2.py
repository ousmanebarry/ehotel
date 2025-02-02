import unittest
from flask import current_app
from flask_testing import TestCase
from main import create_app
from db.db_drivers import Database
from config import TestConfig
from flask_jwt_extended import decode_token, get_jwt
import json

app_instance = None

class TestAvailableRooms(TestCase):

    def create_app(self):
        global app_instance

        if app_instance is None:
            app_instance = create_app(TestConfig)

        return app_instance

    def test_get_available_rooms(self):
        # Test data
        start_date = "2023-04-03"
        end_date = "2023-04-25"

        # Make a request to the /room/available-rooms endpoint
        response = self.client.get(f"/room/available-rooms?start_date={start_date}&end_date={end_date}")
        print(f"response {response.json}")

        # Check if the response is successful
        self.assertEqual(response.status_code, 200, f"Failed to get available rooms: {response.data}")

        # Check if the response contains the expected data
        expected_data = [
            {"country": "USA", "state_province": "NY", "city": "New York", "available_rooms": 1},
            {"country": "USA", "state_province": "CA", "city": "San Francisco", "available_rooms": 2},
        ]
        self.assertEqual(response.json, expected_data, "Response data does not match expected data")

    import unittest
from flask import current_app
from flask_testing import TestCase
from main import create_app
from db.db_drivers import Database
from config import TestConfig
from flask_jwt_extended import decode_token, get_jwt
import json

app_instance = None

class TestAvailableRooms(TestCase):

    def create_app(self):
        global app_instance

        if app_instance is None:
            app_instance = create_app(TestConfig)

        return app_instance

    def test_hotel_search(self):
        # Test data
        star_rating = 4
        room_capacity = 2
        is_extendable = True
        price_per_night = 150

        # Make a request to the /hotel/search endpoint
        response = self.client.get(f"hotel/hotel/search?star_rating={star_rating}&room_capacity={room_capacity}&is_extendable={is_extendable}&price_per_night={price_per_night}")
        print(f"response {response.json}")

        # Check if the response is successful
        self.assertEqual(response.status_code, 200, f"Failed to search hotels: {response.data}")

        # Check if the response contains the expected data
        # Replace the example data with the expected data from your test database
        expected_data = [{'hotel_ID': 1, 'chain_ID': 1, 'number_of_rooms': 200, 'address_street_name': 'Main St', 'address_street_number': 123, 'address_city': 'New York', 'address_province_state': 'NY', 'address_country': 'USA', 'contact_email': 'hilton1@example.com', 'star_rating': 5, 'rooms': [{'room_number': 1, 'room_capacity': 2, 'view_type': 'city', 'price_per_night': 100, 'is_extendable': True, 'room_problems': ''}]}]
        # self.assertEqual(response.json, expected_data, "Response data does not match expected data")

if __name__ == "__main__":
    unittest.main()

