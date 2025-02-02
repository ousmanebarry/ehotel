from flask import request
from flask import current_app
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from datetime import date

rental_namespace = Namespace("rental", description="All routes under this namespace concern rental operations.")

create_rental_model = rental_namespace.model('CreateRental', {
    'total_paid': fields.Integer(required=True, description='Total amount paid for the rental'),
    'discount': fields.Integer(required=True, description='Discount applied to the rental'),
    'additional_charges': fields.Integer(required=True, description='Additional charges for the rental'),
    'check_in_date': fields.Date(required=True, description='Check-in date'),
    'check_out_date': fields.Date(required=True, description='Check-out date'),
    'customer_SSN_SIN': fields.Integer(required=True, description='Customer SSN/SIN'),
    'room_number': fields.Integer(required=True, description='Room number'),
    'hotel_ID': fields.Integer(required=True, description='Hotel ID'),
    'employee_ID': fields.Integer(required=True, description='Employee ID'),
})

conv_booking_to_rental_model = rental_namespace.model('ConvertToRental', {
    'employee_ID': fields.Integer(required=True, description='Employee ID'),
    'total_paid': fields.Integer(required=True, description='Total amount paid for the rental'),
    'discount': fields.Integer(required=True, description='Discount applied to the rental'),
    'additional_charges': fields.Integer(required=True, description='Additional charges for the rental'),
})

@rental_namespace.route("/rental")
class Rental(Resource):
    @rental_namespace.doc(responses={201: "Created", 400: "Invalid input", 401: "Unauthorized"})
    @rental_namespace.expect(create_rental_model)
    @jwt_required()
    def post(self):
        token_data = get_jwt()
        if token_data["role"] != "employee":
            return {"message": "Unauthorized!"}, 401

        employee_SSN_SIN = get_jwt_identity()
        data = request.json
        try:
            success, message = current_app.db.create_rental(
                employee_SSN_SIN,
                data["employee_ID"],
                data["room_number"],
                data["hotel_ID"],
                data["customer_SSN_SIN"],
                date(*map(int, data["check_in_date"].split("-"))),
                date(*map(int, data["check_out_date"].split("-"))),
                data.get("total_paid", None),
                data.get("discount", None),
                data.get("additional_charges", None)
            )
            if not success:
                return {"message": message}, 400
        except Exception as e:
            return {"message": str(e)}, 400

        return {"message": message}, 201


@rental_namespace.route("/rentals/<int:customer_SSN_SIN>")
class RentalsByCustomer(Resource):
    @rental_namespace.doc(responses={200: "Success", 401: "Unauthorized", 500: "Internal Server Error"})
    @jwt_required()
    def get(self, customer_SSN_SIN=None):
        token_data = get_jwt()
        role = token_data["role"]
        user_SSN_SIN = get_jwt_identity()

        if role == "customer" and customer_SSN_SIN != user_SSN_SIN:
            return {"message": "Unauthorized!"}, 401

        try:
            if role == "employee" and customer_SSN_SIN is None:
                rentals = current_app.db.get_all_rentals()
            else:
                rentals = current_app.db.get_rentals_by_customer(customer_SSN_SIN)

            parsed_rentals = [
                {
                    "rental_ID": rental[0],
                    "base_price": rental[1],
                    "date_paid": rental[2].isoformat(),
                    "total_paid": rental[3],
                    "discount": rental[4],
                    "additional_charges": rental[5],
                    "check_in_date": rental[6].isoformat(),
                    "check_out_date": rental[7].isoformat(),
                    "customer_SSN_SIN": rental[8],
                    "booking_ID": rental[9],
                    "room_number": rental[10],
                    "hotel_ID": rental[11],
                    "employee_ID": rental[12],
                    "employee_SSN_SIN": rental[13]
                }
                for rental in rentals
            ]

            return parsed_rentals, 200
        except Exception as e:
            return {"message": f"Error getting rentals: {str(e)}"}, 500


@rental_namespace.route("/rental/convert/<int:booking_id>")
class ConvertBookingToRental(Resource):
    @rental_namespace.doc(responses={201: "Created", 400: "Invalid input", 401: "Unauthorized"})
    @rental_namespace.expect(conv_booking_to_rental_model)
    @jwt_required()
    def post(self, booking_id):

        employee_ssn_sin = get_jwt_identity()
        token_data = get_jwt()
        data = request.json
        employee_id = data.get("employee_id", None)

        if token_data["role"] != "employee":
            return {"message": "Unauthorized!"}, 401
        
        if not employee_id: 
            return {"message": "Employee ID not provided."}, 400

        employee = current_app.db.get_employee(employee_ssn_sin=employee_ssn_sin)

        if not employee or employee[1] != employee_id:
            return {"message": "Employee ID mismatch or employee not found!"}, 401

        success, message = current_app.db.convert_booking_to_rental(
            booking_id,
            employee_ssn_sin,
            employee_id,
            data.get("total_paid", None),
            data.get("discount", None),
            data.get("additional_charges", None)
        )

        if not success:
            return {"message": message}, 400

        return {"message": message}, 201