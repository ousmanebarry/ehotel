from flask_restx import Resource, Namespace, fields
from flask import current_app
from flask import Flask, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash
from datetime import datetime

auth_namespace = Namespace("auth", description="All routes under this namespace concern authentication of customers and employees.")

customer_model = auth_namespace.model('Customer', {
    'customer_SSN_SIN': fields.Integer(required=True, description='Customer SSN/SIN'),
    'first_name': fields.String(required=True, description='First name of the customer'),
    'last_name': fields.String(required=True, description='Last name of the customer'),
    'password': fields.String(required=True, description='Password of the customer'), 
    'address_street_name': fields.String(required=True, description='Street name of the customer address'),
    'address_street_number': fields.Integer(required=True, description='Street number of the customer address'),
    'address_city': fields.String(required=True, description='City of the customer address'),
    'address_province_state': fields.String(required=True, description='Province or state of the customer address'),
    'address_country': fields.String(required=True, description='Country of the customer address')
})

customer_update_model = auth_namespace.model('CustomerUpdateModel', {
    'customer_SSN_SIN': fields.Integer(required=True, description='Customer SSN/SIN'),
    'first_name': fields.String(required=False, description='First name of the customer'),
    'last_name': fields.String(required=False, description='Last name of the customer'),
    'address_street_name': fields.String(required=False, description='Street name of the customer address'),
    'address_street_number': fields.Integer(required=False, description='Street number of the customer address'),
    'address_city': fields.String(required=False, description='City of the customer address'),
    'address_province_state': fields.String(required=False, description='Province or state of the customer address'),
    'address_country': fields.String(required=False, description='Country of the customer address')
})

employee_model = auth_namespace.model('Employee', {
    'employee_SSN_SIN': fields.Integer(required=True, description='Employee SSN/SIN'),
    'employee_ID': fields.Integer(required=True, description='Employee ID'),
    'first_name': fields.String(required=True, description='First name of the employee'),
    'last_name': fields.String(required=True, description='Last name of the employee'),
    'password': fields.String(required=True, description='Password of the employee'),
    'address_street_name': fields.String(required=True, description='Street name of the employee address'),
    'address_street_number': fields.Integer(required=True, description='Street number of the employee address'),
    'address_city': fields.String(required=True, description='City of the employee address'),
    'address_province_state': fields.String(required=True, description='Province or state of the employee address'),
    'address_country': fields.String(required=True, description='Country of the employee address'),
    'hotel_ID': fields.Integer(required=True, description='Hotel ID where the employee works'),
    'is_manager': fields.Boolean(required=True, description='Indicates if the employee is a manager'),
    'role': fields.String(required=True, description='Role of the employee at the hotel')
})

employee_update_model = auth_namespace.model('EmployeeUpdateModel', {
    'employee_SSN_SIN': fields.Integer(required=True, description='Employee SSN/SIN'),
    'employee_ID': fields.Integer(required=True, description='Employee ID'),
    'first_name': fields.String(required=False, description='First name of the employee'),
    'last_name': fields.String(required=False, description='Last name of the employee'),
    'address_street_name': fields.String(required=False, description='Street name of the employee address'),
    'address_street_number': fields.Integer(required=False, description='Street number of the employee address'),
    'address_city': fields.String(required=False, description='City of the employee address'),
    'address_province_state': fields.String(required=False, description='Province or state of the employee address'),
    'address_country': fields.String(required=False, description='Country of the employee address'),
    'hotel_ID': fields.Integer(required=False, description='Hotel ID where the employee works'),
    'is_manager': fields.Boolean(required=False, description='Indicates if the employee is a manager'),
    'role': fields.String(required=False, description='Role of the employee at the hotel')
})

login_model = auth_namespace.model("Login", {
    "user_SSN_SIN": fields.Integer(),
    "password": fields.String(),
    "role": fields.String()
})

add_employee_role_model = auth_namespace.model('AddEmployeeRole', {
    'employee_SSN_SIN': fields.Integer(required=True, description='Employee SSN/SIN'),
    'employee_ID': fields.Integer(required=True, description='Employee ID'),
    'role': fields.String(required=True, description='Role of the employee at the hotel')
})

@auth_namespace.route("/customers")
class CustomerRegistration(Resource):
    @auth_namespace.doc(responses={200: "Success", 400: "Invalid input", 409: "Conflict", 500: "Internal Server Error"})
    @auth_namespace.expect(customer_model)
    def post(self):

        data = request.json

        required_fields = [
            'customer_SSN_SIN', 'first_name', 'last_name', 'password', 'address_street_name',
            'address_street_number', 'address_city', 'address_province_state', 'address_country'
        ]

        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return {"message": f"Missing required fields: {', '.join(missing_fields)}"}, 400

        ssn_sin = data["customer_SSN_SIN"]
        first_name = data["first_name"]
        last_name = data["last_name"]
        password = data["password"]
        address_street_name = data["address_street_name"]
        address_street_number = data["address_street_number"]
        address_city = data["address_city"]
        address_province_state = data["address_province_state"]
        address_country = data["address_country"]
        registration_date = datetime.today()

        hashed_password = generate_password_hash(password)

        success, message = current_app.db.insert_customer(
            ssn_sin, hashed_password, first_name,
            last_name, address_street_name,
            address_street_number, address_city,
            address_province_state, address_country,
            registration_date
        )

        if success:
            return {"message": message}, 200
        else:
            if message == "Error: Customer or Employee with the same SSN/SIN already exists.":
                return {"message": message}, 409
            else: 
                return {"message": message}, 500


@auth_namespace.route("/employees")
class EmployeeRegistration(Resource):
    @auth_namespace.doc(responses={200: "Success", 400: "Invalid input", 409: "Conflict", 500: "Internal Server Error"})
    @auth_namespace.expect(employee_model)
    def post(self):
        data = request.json

        ssn_sin = data["employee_SSN_SIN"]
        employee_id = data["employee_ID"]
        first_name = data["first_name"]
        last_name = data["last_name"]
        password = data["password"]
        address_street_name = data["address_street_name"]
        address_street_number = data["address_street_number"]
        address_city = data["address_city"]
        address_province_state = data["address_province_state"]
        address_country = data["address_country"]
        hotel_id = data["hotel_ID"]
        is_manager = data["is_manager"]
        role = data["role"]

        try:
            # Hash the password
            hashed_password = generate_password_hash(password)

            # Insert the employee and their role
            success, message = current_app.db.insert_employee(
                ssn_sin, employee_id, hashed_password, first_name,
                last_name, address_street_name,
                address_street_number, address_city,
                address_province_state, address_country,
                hotel_id, is_manager
            )

            if not success:
                if message == "Error: Customer or Employee with the same SSN/SIN already exists.":
                    return {"message": message}, 409
                else: 
                    return {"message": message}, 500

            success, message = current_app.db.insert_employee_role(
                employee_SSN_SIN=ssn_sin, employee_ID=employee_id, role=role
            )

            if not success:
                if message == "Error: Employee already possesses the role.":
                    return {"message": message}, 409
                else: 
                    return {"message": message}, 500

            return {"message": "Employee registered successfully."}, 200

        except Exception as e:
            return {"message": f"Error: {str(e)}"}, 500


@auth_namespace.route("/login")
class Login(Resource):
    @auth_namespace.doc(responses={200: "Success", 400: "Invalid input", 401: "Unauthorized", 500: "Internal Server Error"})
    @auth_namespace.expect(login_model)
    def post(self):
        data = request.json
        user_ssn_sin = data.get("user_SSN_SIN")
        password = data.get("password")
        role = data.get("role")

        # Validate input
        if not user_ssn_sin or not password or not role:
            return {"message": "User SSN/SIN, password, and role are required."}, 400

        # Check if the user exists in the database and verify the role
        result = current_app.db.check_account_and_role(user_ssn_sin, password, role)
        if result[0] == "Invalid SSN/SIN" or result[0] == "Invalid Password" or result[0] == "Invalid Role":
            return {"message": result[0]}, 401

        if role == "employee":
          token_data = {
                  "user_ssn_sin": user_ssn_sin,
                  "first_name": result[2][2],
                  "last_name": result[2][3],
                  "role": role,
              }
        else:
          token_data = {
                  "user_ssn_sin": user_ssn_sin,
                  "first_name": result[2][1],
                  "last_name": result[2][2],
                  "role": role,
              }
        
        is_manager = False

        if result[1] == "employee":
            if result[2][10]:
                is_manager = True

            # Create the JWT token with is_manager included
            token_data["is_manager"] = is_manager 
            token_data["hotel_id"] = result[2][9]

        access_token = create_access_token(identity=user_ssn_sin, additional_claims=token_data)

        # Return the access token
        return {"access_token": access_token}, 200


@auth_namespace.route("/customers/<int:customer_SSN_SIN>")
class CustomerUpdate(Resource):
    @jwt_required()
    @auth_namespace.expect(customer_update_model)
    def put(self, customer_SSN_SIN):
        data = request.json

        # Get the current user's SSN/SIN and role from the JWT token
        current_user_ssn_sin = get_jwt_identity()
        current_user_role = get_jwt().get("role")

        # Only allow customers to update their own information
        if current_user_role == "customer" and current_user_ssn_sin != customer_SSN_SIN:
            return {"message": "Unauthorized"}, 401

        # Parse the data and pass it to the update_customer function
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        address_street_name = data.get("address_street_name")
        address_street_number = data.get("address_street_number")
        address_city = data.get("address_city")
        address_province_state = data.get("address_province_state")
        address_country = data.get("address_country")
        success, message = current_app.db.update_customer(
            customer_SSN_SIN, first_name, last_name,
            address_street_name, address_street_number,
            address_city, address_province_state, address_country
        )

        if success:
            return {"message": message}, 200
        else:
            return {"message": message}, 500


@auth_namespace.route("/customers/<int:customer_SSN_SIN>")
class CustomerDetails(Resource):
    @jwt_required()
    def get(self, customer_SSN_SIN):
        # Get the current user's SSN/SIN and role from the JWT token
        current_user_ssn_sin = get_jwt_identity()
        jwt_claims = get_jwt()
        is_manager = jwt_claims.get("is_manager", False)

        # Only allow managers or customers to see customer information
        if is_manager or current_user_ssn_sin == customer_SSN_SIN:
            # Get the customer's information from the database
            customer_info = current_app.db.get_customer(customer_SSN_SIN)
            if customer_info:
                # Convert the result into a dictionary
                customer_dict = {
                    "customer_SSN_SIN": customer_info[0][0],
                    "first_name": customer_info[0][1],
                    "last_name": customer_info[0][2],
                    "address_street_name": customer_info[0][3],
                    "address_street_number": customer_info[0][4],
                    "address_city": customer_info[0][5],
                    "address_province_state": customer_info[0][6],
                    "address_country": customer_info[0][7],
                    "registration_date": customer_info[0][8].strftime("%Y-%m-%d")
                }
                return customer_dict, 200
            else:
                return {"message": "Customer not found."}, 404
        else:
            return {"message": "Unauthorized"}, 401


@auth_namespace.route("/employees/<int:employee_SSN_SIN>")
class EmployeeUpdate(Resource):
    @jwt_required()
    @auth_namespace.expect(employee_update_model)
    def put(self, employee_SSN_SIN):
        data = request.json

        # Get the current user's SSN/SIN and role from the JWT token
        current_user_ssn_sin = get_jwt_identity()
        jwt_claims = get_jwt()
        is_manager = jwt_claims.get("is_manager", False)

        # Only allow managers or employees to update their own information
        if not is_manager and current_user_ssn_sin != employee_SSN_SIN:
            return {"message": "Unauthorized"}, 401

        # Parse the data and pass it to the update_employee function
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        address_street_name = data.get("address_street_name")
        address_street_number = data.get("address_street_number")
        address_city = data.get("address_city")
        address_province_state = data.get("address_province_state")
        address_country = data.get("address_country")
        hotel_ID = data.get("hotel_ID")
        employee_ID = data.get("employee_ID")
        promote_to_manager = data.get("promote_to_manager")
        demote_from_manager = data.get("demote_from_manager")

        success, message = current_app.db.update_employee(
            employee_SSN_SIN, employee_ID, first_name, last_name,
            address_street_name, address_street_number,
            address_city, address_province_state, address_country,
            hotel_ID, promote_to_manager, demote_from_manager
        )

        if success:
            return {"message": message}, 200
        else:
            return {"message": message}, 500


@auth_namespace.route("/employees/<int:employee_SSN_SIN>")
class EmployeeDetails(Resource):
    @jwt_required()
    def get(self, employee_SSN_SIN):
        
        # Get the current user's SSN/SIN and role from the JWT token
        current_user_ssn_sin = get_jwt_identity()
        jwt_claims = get_jwt()
        is_manager = jwt_claims.get("is_manager", False)

        # Only allow managers or employees to see their own information
        if not is_manager and current_user_ssn_sin != employee_SSN_SIN:
            return {"message": "Unauthorized"}, 401

        # Get the employee's information from the database
        employee_info = current_app.db.get_employee(employee_SSN_SIN)

        if employee_info:
            # Convert the result into a dictionary
            employee_dict = {
                "employee_SSN_SIN": employee_info[0],
                "employee_ID": employee_info[1],
                "first_name": employee_info[2],
                "last_name": employee_info[3],
                "address_street_name": employee_info[4],
                "address_street_number": employee_info[5],
                "address_city": employee_info[6],
                "address_province_state": employee_info[7],
                "address_country": employee_info[8],
                "hotel_ID": employee_info[9],
                "is_manager": employee_info[10]
            }
            return employee_dict, 200
        else:
            return {"message": "Employee not found."}, 404
