from flask import Flask, request, jsonify
from flask import current_app
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, get_jwt

hotel_namespace = Namespace("hotel", description="All routes under this namespace concern hotel operations.")

hotel_model = hotel_namespace.model('Hotel', {
    'hotel_ID': fields.Integer(required=True, description='Hotel ID'),
    'chain_ID': fields.Integer(required=True, description='Hotel chain ID'),
    'number_of_rooms': fields.Integer(required=True, description='Number of rooms in the hotel'),
    'address_street_name': fields.String(required=True, description='Street name of the hotel address'),
    'address_street_number': fields.Integer(required=True, description='Street number of the hotel address'),
    'address_city': fields.String(required=True, description='City of the hotel address'),
    'address_province_state': fields.String(required=True, description='Province or state of the hotel address'),
    'address_country': fields.String(required=True, description='Country of the hotel address'),
    'contact_email': fields.String(required=True, description='Contact email of the hotel'),
    'star_rating': fields.Integer(required=True, description='Star rating of the hotel')
})

hotel_update_model = hotel_namespace.model('HotelUpdate', {
    'hotel_ID': fields.Integer(required=True, description='Hotel ID'),
    'chain_ID': fields.Integer(required=True, description='Hotel chain ID'),
    'number_of_rooms': fields.Integer(required=False, description='Number of rooms in the hotel'),
    'address_street_name': fields.String(required=False, description='Street name of the hotel address'),
    'address_street_number': fields.Integer(required=False, description='Street number of the hotel address'),
    'address_city': fields.String(required=False, description='City of the hotel address'),
    'address_province_state': fields.String(required=False, description='Province or state of the hotel address'),
    'address_country': fields.String(required=False, description='Country of the hotel address'),
    'contact_email': fields.String(required=False, description='Contact email of the hotel'),
    'star_rating': fields.Integer(required=False, description='Star rating of the hotel')
})


@hotel_namespace.route("/hotel")
class Hotel(Resource):
    @hotel_namespace.doc(responses={201: "Created", 401: "Unauthorized", 409: "Conflict", 500: "Internal Server Error"})
    @hotel_namespace.expect(hotel_model)
    @jwt_required()
    def post(self):
        token_data = get_jwt()
        if not token_data.get("is_manager", False):
            return {"message": "Unauthorized!"}, 401
        data = request.json
        hotel_id = data["hotel_ID"]
        chain_id = data["chain_ID"]
        number_of_rooms = data["number_of_rooms"]
        address_street_name = data["address_street_name"]
        address_street_number = data["address_street_number"]
        address_city = data["address_city"]
        address_province_state = data["address_province_state"]
        address_country = data["address_country"]
        contact_email = data["contact_email"]
        star_rating = data["star_rating"]

        try:
            existing_hotel = current_app.db.get_hotel(hotel_id)
            if existing_hotel:
                return {"message": "Hotel with the given ID already exists."}, 409

            current_app.db.insert_hotel(hotel_id, chain_id, number_of_rooms, address_street_name, address_street_number, address_city, address_province_state, address_country, contact_email, star_rating)
            return {"message": "Hotel added successfully."}, 201

        except Exception as e:
            return {"message": f"Error adding hotel: {e}"}, 500


    @hotel_namespace.doc(responses={200: "Success", 400: "Invalid input", 401: "Unauthorized", 500: "Internal Server Error"})
    @hotel_namespace.expect(hotel_update_model)
    @jwt_required()
    def put(self):
        token_data = get_jwt()
        if not token_data.get("is_manager", False):
            return {"message": "Only managers can edit hotels"}, 401

        data = request.json
        hotel_id = data["hotel_ID"]
        chain_id = data["chain_ID"]
        number_of_rooms = data.get("number_of_rooms")
        address_street_name = data.get("address_street_name")
        address_street_number = data.get("address_street_number")
        address_city = data.get("address_city")
        address_province_state = data.get("address_province_state")
        address_country = data.get("address_country")
        contact_email = data.get("contact_email")
        star_rating = data.get("star_rating")

        try:
            existing_hotel = current_app.db.get_hotel(hotel_id)
            if not existing_hotel:
                return {"message": "Hotel with the given ID does not exist."}, 404

            current_app.db.insert_hotel(hotel_id, chain_id, number_of_rooms, address_street_name, address_street_number, address_city, address_province_state, address_country, contact_email, star_rating)
            return {"message": "Hotel updated successfully."}, 200

        except Exception as e:
            return {"message": f"Error updating hotel: {e}"}, 500
        
    @hotel_namespace.doc(responses={200: "Success", 500: "Internal Server Error"})
    def get(self):
        try:
            hotels = current_app.db.get_all_hotels()
            return hotels, 200

        except Exception as e:
            return {"message": f"Error getting hotels: {e}"}, 500
    

@hotel_namespace.route("/hotel/search")
class HotelSearch(Resource):
    @hotel_namespace.doc(responses={200: "Success", 500: "Internal Server Error"})
    def get(self):
        start_date = request.args.get('start_date', None)
        end_date = request.args.get('end_date', None)
        hotel_chain = request.args.get('hotel_chain', None)
        city = request.args.get('city', None)
        star_rating = request.args.get('star_rating', None)
        view_type = request.args.get('view_type', None)
        room_capacity = request.args.get('room_capacity', None)
        is_extendable = request.args.get('is_extendable', None)
        price_per_night = request.args.get('price_per_night', None)
        start_date = request.args.get('start_date', None)

        if not start_date or not end_date:
            return {"message": "Start date and end date are required."}, 400

        try:
            hotels = current_app.db.search_hotels_and_rooms(start_date=start_date, end_date=end_date, hotel_chain=hotel_chain, city=city, star_rating=star_rating, view_type=view_type, room_capacity=room_capacity, is_extendable=is_extendable, price_per_night=price_per_night)
            return hotels, 200

        except Exception as e:
            return {"message": f"Error searching hotels: {e}"}, 500


@hotel_namespace.route("/hotel/<int:hotel_ID>")
class HotelByID(Resource):
    @hotel_namespace.doc(responses={200: "Success", 404: "Not found", 500: "Internal Server Error"})
    def get(self, hotel_ID):
        try:
            hotel = current_app.db.get_hotel(hotel_ID)
            if not hotel:
                return {"message": "Hotel not found."}, 404

            hotel_json = {
                'hotel_ID': hotel[0],
                'chain_ID': hotel[1],
                'number_of_rooms': hotel[2],
                'address_street_name': hotel[3],
                'address_street_number': hotel[4],
                'address_city': hotel[5],
                'address_province_state': hotel[6],
                'address_country': hotel[7],
                'contact_email': hotel[8],
                'star_rating': hotel[9]
            }
            return hotel_json, 200

        except Exception as e:
            return {"message": f"Error retrieving hotel: {e}"}, 500

    @hotel_namespace.doc(responses={200: "Success", 401: "Unauthorized", 404: "Not found", 500: "Internal Server Error"})
    @jwt_required()
    def delete(self, hotel_ID):
        token_data = get_jwt()
        if not token_data.get("is_manager", False):
            return {"message": "Only managers can delete hotels"}, 401

        try:
            existing_hotel = current_app.db.get_hotel(hotel_ID)
            if not existing_hotel:
                return {"message": "Hotel with the given ID does not exist."}, 404

            current_app.db.delete_hotel(hotel_ID)
            return {"message": "Hotel removed successfully."}, 200

        except Exception as e:
            return {"message": f"Error removing hotel: {e}"}, 500


@hotel_namespace.route("/hotel/total_capacity")
class TotalCapacity(Resource):
    @hotel_namespace.doc(responses={200: "Success", 404: "Not found", 500: "Internal Server Error"})
    def get(self):
        try:
            total_capacity = current_app.db.get_rooms_capacity()
            if total_capacity == None:
                return {"message": "Hotel not found or hotel has no rooms."}, 404
            
            output = []
            for result in total_capacity:
                output.append({
                    "hotel_chain_name": result[0],
                    "chain_id": result[1],
                    "hotel_id": result[2],
                    "room_number": result[3],
                    "room_capacity": result[4]
                })

            return output, 200

        except Exception as e:
            return {"message": f"Error retrieving total capacity: {e}"}, 500

@hotel_namespace.route("/hotel/total_capacity/<int:hotel_ID>")
class HotelTotalCapacity(Resource):
    @hotel_namespace.doc(responses={200: "Success", 404: "Not found", 500: "Internal Server Error"})
    def get(self, hotel_ID):
        try:
            total_capacity = current_app.db.get_rooms_capacity_by_hotel(hotel_ID)
            if total_capacity == None:
                return {"message": "Hotel not found or hotel has no rooms."}, 404
            
            output = []
            for result in total_capacity:
                output.append({
                    "hotel_chain_name": result[0],
                    "chain_id": result[1],
                    "hotel_id": result[2],
                    "room_number": result[3],
                    "room_capacity": result[4]
                })

            return output, 200

        except Exception as e:
            return {"message": f"Error retrieving total capacity: {e}"}, 500