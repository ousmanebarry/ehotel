from flask import Flask, request, jsonify
from flask import current_app
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, get_jwt
from datetime import datetime

room_namespace = Namespace(
    "room", description="All routes under this namespace concern room operations.")

room_model = room_namespace.model('Room', {
    'room_number': fields.Integer(required=True, description='Room number'),
    'hotel_ID': fields.Integer(required=True, description='Hotel ID'),
    'room_capacity': fields.Integer(required=True, description='Capacity of the room'),
    'view_type': fields.String(required=True, description='View type of the room'),
    'price_per_night': fields.Integer(required=True, description='Price per night for the room'),
    'is_extendable': fields.Boolean(required=True, description='Indicates if the room is extendable'),
    'room_problems': fields.String(required=False, description='Problems associated with the room')
})

room_update_model = room_namespace.model('RoomUpdate', {
    'room_number': fields.Integer(required=True, description='Room number'),
    'hotel_ID': fields.Integer(required=True, description='Hotel ID'),
    'room_capacity': fields.Integer(required=False, description='Capacity of the room'),
    'view_type': fields.String(required=False, description='View type of the room'),
    'price_per_night': fields.Integer(required=False, description='Price per night for the room'),
    'is_extendable': fields.Boolean(required=False, description='Indicates if the room is extendable'),
    'room_problems': fields.String(required=False, description='Problems associated with the room')
})


@room_namespace.route("/room")
class Room(Resource):
    @room_namespace.doc(
        responses={
            201: "Created",
            401: "Unauthorized",
            409: "Conflict",
            500: "Internal Server Error",
        }
    )
    @room_namespace.expect(room_model)
    @jwt_required()
    def post(self):
        token_data = get_jwt()
        if not token_data.get("is_manager", False):
            return {"message": "Only managers can create rooms"}, 401

        data = request.json
        room_number = data["room_number"]
        hotel_id = data["hotel_ID"]
        room_capacity = data["room_capacity"]
        view_type = data["view_type"]
        price_per_night = data["price_per_night"]
        is_extendable = data["is_extendable"]
        room_problems = data.get("room_problems")

        try:
            existing_room = current_app.db.get_room(room_number, hotel_id)
            if existing_room:
                return (
                    {"message": "Room with the given number already exists in the hotel."},
                    409,
                )

            current_app.db.insert_room(
                room_number,
                hotel_id,
                room_capacity,
                view_type,
                price_per_night,
                is_extendable,
                room_problems,
            )
            return {"message": "Room added successfully."}, 201

        except Exception as e:
            return {"message": f"Error adding room: {e}"}, 500

    def get(self):
        rooms = current_app.db.get_all_rooms_with_hotel_info()

        formatted_rooms = []
        for room in rooms:
            formatted_rooms.append({
                "room": {
                    'room_number': room[0],
                    'hotel_ID': room[1],
                    'room_capacity': room[2],
                    'view_type': room[3],
                    'price_per_night': room[4],
                    'is_extendable': room[5],
                    'room_problems': room[6],
                },
                "hotel": {
                    'hotel_ID': room[1],
                    'chain_id': room[8],
                    'number_of_rooms': room[9],
                    'address_street_name': room[10],
                    'address_street_number': room[11],
                    'address_city': room[12],
                    'address_province_state': room[13],
                    'address_country': room[14],
                    'contact_email': room[15],
                    'star_rating': room[16]
                }
          })          

        return formatted_rooms, 200

    @room_namespace.doc(
        responses={
            200: "Success",
            401: "Unauthorized",
            404: "Not found",
            500: "Internal Server Error",
        }
    )
    @room_namespace.expect(room_update_model)
    @jwt_required()
    def put(self):
        token_data = get_jwt()
        if not token_data.get("is_manager", False):
            return {"message": "Unauthorized!"}, 401

        data = request.json
        room_number = data["room_number"]
        hotel_id = data["hotel_ID"]
        room_capacity = data.get("room_capacity")
        view_type = data.get("view_type")
        price_per_night = data.get("price_per_night")
        is_extendable = data.get("is_extendable")
        room_problems = data.get("room_problems")

        try:
            existing_room = current_app.db.get_room(room_number, hotel_id)
            if not existing_room:
                return (
                    {"message": "Room with the given number does not exist in the hotel."},
                    404,
                )

            current_app.db.insert_room(
                room_number,
                hotel_id,
                room_capacity,
                view_type,
                price_per_night,
                is_extendable,
                room_problems,
            )
            return {"message": "Room updated successfully."}, 200

        except Exception as e:
            return {"message": f"Error updating room: {e}"}, 500


@room_namespace.route("/room/<int:hotel_ID>/<int:room_number>")
class RoomByID(Resource):
    @room_namespace.doc(responses={200: "Success", 404: "Not found", 500: "Internal Server Error"})
    def get(self, hotel_ID, room_number):
        try:
            room = current_app.db.get_room(room_number, hotel_ID)
            if not room:
                return {"message": "Room not found."}, 404

            room_json = {
                'room_number': room[0],
                'hotel_ID': room[1],
                'room_capacity': room[2],
                'view_type': room[3],
                'price_per_night': room[4],
                'is_extendable': room[5],
                'room_problems': room[6]
            }
            return room_json, 200

        except Exception as e:
            return {"message": f"Error retrieving room: {e}"}, 500

    @room_namespace.doc(responses={200: "Success", 401: "Unauthorized", 404: "Not found", 500: "Internal Server Error"})
    @jwt_required()
    def delete(self, hotel_ID, room_number):
        token_data = get_jwt()
        if not token_data.get("is_manager", False):
            return {"message": "Unauthorized!"}, 401

        try:
            room = current_app.db.get_room(room_number, hotel_ID)
            if not room:
                return {"message": "Room not found."}, 404

            current_app.db.delete_room(room_number, hotel_ID)
            return {"message": "Room removed successfully."}, 200

        except Exception as e:
            return {"message": f"Error removing room: {e}"}, 500


@room_namespace.route("/available-rooms")
class AvailableRooms(Resource):
    @room_namespace.doc(
        params={
            "start_date": "Start date for the period (YYYY-MM-DD format)",
            "end_date": "End date for the period (YYYY-MM-DD format)",
        },
        responses={
            200: "Success",
            400: "Bad Request",
            500: "Internal Server Error",
        },
    )
    def get(self):
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        if not start_date or not end_date:
            return {"message": "Both start_date and end_date parameters are required."}, 400

        date_format = "%Y-%m-%d"
        try:
            start_date = datetime.strptime(start_date, date_format).date()
            end_date = datetime.strptime(end_date, date_format).date()
        except ValueError:
            return {"message": "Invalid date format. Please use YYYY-MM-DD format."}, 400
        
        if start_date >= end_date:
            return {"message": "Start date cannot be later than or to equal to end date."}, 400

        try:
            rooms_per_area = current_app.db.get_rooms_per_area_by_date(start_date, end_date)
            result = [
                {
                    "country": item[0],
                    "state_province": item[1],
                    "city": item[2],
                    "available_rooms": item[3],
                }
                for item in rooms_per_area
            ]
            return result
        except Exception as e:
            return {"message": f"Error retrieving available rooms: {e}"}, 500