from flask import Flask, request, jsonify
from flask import current_app
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, get_jwt
from datetime import date

booking_namespace = Namespace("booking", description="All routes under this namespace concern booking operations.")

booking_model = booking_namespace.model('Booking', {
    'scheduled_check_in_date': fields.Date(required=True, description='Scheduled check-in date'),
    'scheduled_check_out_date': fields.Date(required=True, description='Scheduled check-out date'),
    'canceled': fields.Boolean(required=True, description='Indicates if the booking is canceled'),
    'room_number': fields.Integer(required=True, description='Room number'),
    'hotel_ID': fields.Integer(required=True, description='Hotel ID')
})

booking_update_model = booking_namespace.model('Booking', {
    'scheduled_check_in_date': fields.Date(required=False, description='Scheduled check-in date'),
    'scheduled_check_out_date': fields.Date(required=False, description='Scheduled check-out date'),
    'canceled': fields.Boolean(required=False, description='Indicates if the booking is canceled'),
    'room_number': fields.Integer(required=False, description='Room number'),
    'hotel_ID': fields.Integer(required=False, description='Hotel ID')
})

@booking_namespace.route("/booking")
class Booking(Resource):
    @booking_namespace.doc(responses={201: "Created", 400: "Invalid input", 401: "Unauthorized"})
    @booking_namespace.expect(booking_model)
    @jwt_required()
    def post(self):
        token_data = get_jwt()
        if token_data["role"] != "customer":
            return {"message": "Unauthorized!"}, 401

        customer_SSN_SIN = get_jwt_identity()
        data = request.json
        try:
            current_app.db.insert_booking(
                customer_SSN_SIN, 
                data["room_number"], 
                data["hotel_ID"], 
            date(*map(int, data["scheduled_check_in_date"].split('-'))), 
            date(*map(int, data["scheduled_check_out_date"].split('-')))
        )
        except Exception as e:
            return {"message": str(e)}, 400

        return {"message": "Booking added successfully."}, 201

    @booking_namespace.doc(responses={200: "Success", 401: "Unauthorized", 404: "Booking does not exist", 400: "Bad request", 500: "Internal Server Error" })
    @booking_namespace.expect(booking_model)
    @jwt_required()
    def put(self):
        token_data = get_jwt()
        if token_data["role"] != "customer":
            return {"message": "Unauthorized!"}, 401

        customer_SSN_SIN = get_jwt_identity()
        data = request.json
        booking_id = data["booking_ID"]
        room_number = data.get("room_number")
        hotel_id = data.get("hotel_ID")
        check_in_date = data.get("scheduled_check_in_date")
        check_out_date = data.get("scheduled_check_out_date")

        existing_booking = current_app.db.get_booking(booking_id)
        if not existing_booking:
            return {"message": "Booking does not exist."}, 404
        
        if existing_booking[5] != customer_SSN_SIN:
            return {"message": "Unauthorized!"}, 401
        
        if check_in_date and check_out_date and check_in_date >= check_out_date:
            return {"message": "Check-in date must be before check-out date."}, 400
        
        try:
            current_app.db.update_booking(
                booking_id,
                customer_SSN_SIN, 
                room_number,
                hotel_id,
                check_in_date,
                check_out_date,
            )
            return {"message": "Booking updated successfully."}, 200
        except Exception as e:
            return {"message": f"Error updating booking: {str(e)}"}, 500

    @booking_namespace.doc(responses={200: "Success", 401: "Unauthorized", 500: "Internal Server Error"})
    @jwt_required()
    def get(self):
        customer_SSN_SIN = get_jwt_identity()
        try:
            bookings = current_app.db.get_all_bookings(customer_SSN_SIN)
            parsed_bookings = [
                {
                    "booking_ID": booking[0],
                    "booking_date": booking[1].isoformat(),
                    "scheduled_check_in_date": booking[2].isoformat(),
                    "scheduled_check_out_date": booking[3].isoformat(),
                    "canceled": booking[4],
                    "customer_SSN_SIN": booking[5],
                    "room_number": booking[6],
                    "hotel_ID": booking[7]
                }
                for booking in bookings
            ]

            return parsed_bookings, 200
        except Exception as e:
            return {"message": f"Error getting bookings: {str(e)}"}, 500


@booking_namespace.route("/booking/<int:booking_ID>")
class BookingByID(Resource):

    @booking_namespace.doc(responses={200: "Success", 401: "Unauthorized", 404: "Booking does not exist", 500: "Internal Server Error"})
    @jwt_required()
    def delete(self, booking_ID):
        customer_SSN_SIN = get_jwt_identity()
        existing_booking = current_app.db.get_booking(booking_ID)

        if not existing_booking:
            return {"message": "Booking does not exist or already has been cancelled."}, 404
        
        if existing_booking[5] != customer_SSN_SIN:
            return {"message": "Unauthorized!"}, 401
        
        success, message = current_app.db.cancel_booking(booking_ID)
        if success:
            return {"message": message}, 200
        else:
            return {"message": message}, 500


@booking_namespace.route("/employee_bookings/<int:ssn_sin>")
class BookingByCustomerSSN_SIN(Resource):
    @booking_namespace.doc(responses={200: "Success", 401: "Unauthorized", 500: "Internal Server Error", 404: "No Bookings Found"})
    @jwt_required()
    def get(self, ssn_sin):
        token_data = get_jwt()
        if token_data["role"] != "employee":
            return {"message": "Unauthorized!"}, 401
        
        try:
            bookings = current_app.db.get_all_bookings(ssn_sin)
            if not bookings:
                return {"message": "No bookings found for the given customer SSN/SIN."}, 404
            
            parsed_bookings = [
                {
                    "booking_ID": booking[0],
                    "booking_date": booking[1],
                    "scheduled_check_in_date": booking[2],
                    "scheduled_check_out_date": booking[3],
                    "canceled": booking[4],
                    "customer_SSN_SIN": booking[5],
                    "room_number": booking[6],
                    "hotel_ID": booking[7]
                }
                for booking in bookings
            ]

            return parsed_bookings, 200
        except Exception as e:
            return {"message": f"Error getting bookings: {str(e)}"}, 500


@booking_namespace.route("/all_bookings")
class AllBookings(Resource):
    @booking_namespace.doc(responses={200: "Success", 401: "Unauthorized", 500: "Internal Server Error", 404: "No Bookings Found"})
    @jwt_required()
    def get(self):
        token_data = get_jwt()
        if token_data["role"] != "employee":
            return {"message": "Unauthorized!"}, 401
        
        try:
            all_bookings = current_app.db.get_all_bookings()
            if not all_bookings:
                return {"message": "No bookings found."}, 404

            parsed_bookings = [
                {
                    "booking_ID": booking[0],
                    "booking_date": booking[1].isoformat(),
                    "scheduled_check_in_date": booking[2].isoformat(),
                    "scheduled_check_out_date": booking[3].isoformat(),
                    "canceled": booking[4],
                    "customer_SSN_SIN": booking[5],
                    "room_number": booking[6],
                    "hotel_ID": booking[7]
                }
                for booking in all_bookings if not booking[4]
            ]

            return parsed_bookings, 200
        except Exception as e:
            return {"message": f"Error getting all bookings: {str(e)}"}, 500

