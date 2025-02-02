### INPUT MODELS END ###
@api.route('/signup/customer')
class CustomerSignUp(Resource): 
    @api.expect(customer_model)
    def post(self): 
        data = request.get_json()

        
@api.route('/all_hotels')
class Hotels(Resource):
    def get(self): 
        data = request.get_json()
        print(data)
        to_return = jsonify({"message": 'Hotels', "request": data})
        return to_return

@api.route('/hotel_chain/<int:id>')
class Hotel_Chain(Resource): 
    def get(self, id): 
        return {"message": f"Getting hotel chain with id {id}"}

    def post(self, id): 
        return {"message":  f"Adding hotel chain with id {id}"}

    def delete(self, id): 
        return {"message":  f"Deleting hotel chain with id {id}"}

@api.route('/hotel_chain/all_hotels/<int:id>')
class Hotel_Chain(Resource): 
    def get(self, id): 
        return {"message": f"Getting all hotels associated with hotel chain {id}"}

@api.route('/hotel/<int:id>')
class Hotels(Resource): 
    def get(self, id): 
        return {"message": f"Getting hotel with id {id}"}

    def post(self, id): 
        return {"message":  f"Adding hotel with id {id}"}

    def delete(self, id): 
        return {"message":  f"Deleting hotel with id {id}"}

@api.route('/hotel/search')
class HotelSearch(Resource): 
    def get(self): 
        data = request.get_json()
        return {"message": f"Searching for hotels with provided parameters"}

### INPUT MODELS START ###
# Hotel_Chain input model
hotel_chain_model = api.model('HotelChain', {
    'chain_ID': fields.Integer(required=True, description='Hotel chain ID'),
    'name': fields.String(required=True, description='Hotel chain name'),
    'number_of_hotels': fields.Integer(required=True, description='Number of hotels in the chain')
})

# Hotel input model
hotel_model = api.model('Hotel', {
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

# Employee input model
employee_model = api.model('Employee', {
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
    'is_manager': fields.Boolean(required=True, description='Indicates if the employee is a manager')
})

# Employee_Role input model
employee_role_model = api.model('EmployeeRole', {
    'employee_SSN_SIN': fields.Integer(required=True, description='Employee SSN/SIN'),
    'employee_ID': fields.Integer(required=True, description='Employee ID'),
    'hotel_ID': fields.Integer(required=True, description='Hotel ID'),
    'role': fields.String(required=True, description='Role of the employee at the hotel')
})

# Hotel_Phone_Number input model
hotel_phone_number_model = api.model('HotelPhoneNumber', {
    'hotel_ID': fields.Integer(required=True, description='Hotel ID'),
    'phone_number': fields.String(required=True, description='Phone number of the hotel')
})

# Hotel_Chain_Central_Office_Address input model
hotel_chain_central_office_address_model = api.model('HotelChainCentralOfficeAddress', {
    'chain_ID': fields.Integer(required=True, description='Hotel chain ID'),
    'address_street_name': fields.String(required=True, description='Street name of the central office address'),
    'address_street_number': fields.Integer(required=True, description='Street number of the central office address'),
    'address_city': fields.String(required=True, description='City of the central office address'),
    'address_province_state': fields.String(required=True, description='Province or state of the central office address'),
    'address_country': fields.String(required=True, description='Country of the central office address')
})

# Hotel_Chain_Contact_Email input model
hotel_chain_contact_email_model = api.model('HotelChainContactEmail', {
    'chain_ID': fields.Integer(required=True, description='Hotel chain ID'),
    'contact_email': fields.String(required=True, description='Contact email of the hotel chain')
})

# Hotel_Chain_Phone_Number input model
hotel_chain_phone_number_model = api.model('HotelChainPhoneNumber', {
    'chain_ID': fields.Integer(required=True, description='Hotel chain ID'),
    'phone_number': fields.String(required=True, description='Phone number of the hotel chain')
})

# Room input model
room_model = api.model('Room', {
    'room_number': fields.Integer(required=True, description='Room number'),
    'hotel_ID': fields.Integer(required=True, description='Hotel ID'),
    'room_capacity': fields.Integer(required=True, description='Capacity of the room'),
    'view_type': fields.String(required=True, description='View type of the room'),
    'price_per_night': fields.Integer(required=True, description='Price per night for the room'),
    'is_extendable': fields.Boolean(required=True, description='Indicates if the room is extendable'),
    'room_problems': fields.String(required=False, description='Problems associated with the room')
})

# Amenity input model
amenity_model = api.model('Amenity', {
    'amenity_id': fields.Integer(required=True, description='Amenity ID'),
    'amenity_name': fields.String(required=True, description='Amenity name')
})

# Has_Amenity input model
has_amenity_model = api.model('HasAmenity', {
    'amenity_id': fields.Integer(required=True, description='Amenity ID'),
    'hotel_id': fields.Integer(required=True, description='Hotel ID'),
    'room_number': fields.Integer(required=True, description='Room number')
})

# Customer input model
customer_model = api.model('Customer', {
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

# Booking input model
booking_model = api.model('Booking', {
    'booking_ID': fields.Integer(required=True, description='Booking ID'),
    'booking_date': fields.Date(required=True, description='Date of booking'),
    'scheduled_check_in_date': fields.Date(required=True, description='Scheduled check-in date'),
    'scheduled_check_out_date': fields.Date(required=True, description='Scheduled check-out date'),
    'canceled': fields.Boolean(required=True, description='Indicates if the booking is canceled'),
    'customer_SSN_SIN': fields.Integer(required=True, description='Customer SSN/SIN'),
    'room_number': fields.Integer(required=True, description='Room number'),
    'hotel_ID': fields.Integer(required=True, description='Hotel ID')
})

# Rental input model
rental_model = api.model('Rental', {
    'rental_ID': fields.Integer(required=True, description='Rental ID'),
    'base_price': fields.Integer(required=True, description='Base price of the rental'),
    'date_paid': fields.Date(required=True, description='Date the rental was paid'),
    'total_paid': fields.Integer(required=True, description='Total amount paid for the rental'),
    'discount': fields.Integer(required=True, description='Discount applied to the rental'),
    'additional_charges': fields.Integer(required=True, description='Additional charges for the rental'),
    'check_in_date': fields.Date(required=True, description='Check-in date'),
    'check_out_date': fields.Date(required=True, description='Check-out date'),
    'customer_SSN_SIN': fields.Integer(required=True, description='Customer SSN/SIN'),
    'booking_ID': fields.Integer(required=True, description='Booking ID'),
    'room_number': fields.Integer(required=True, description='Room number'),
    'hotel_ID': fields.Integer(required=True, description='Hotel ID'),
    'employee_ID': fields.Integer(required=True, description='Employee ID'),
    'employee_SSN_SIN': fields.Integer(required=True, description='Employee SSN/SIN')
})
