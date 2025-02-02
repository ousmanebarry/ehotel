from flask import request
from flask import current_app
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt

hotel_chain_namespace = Namespace("hotel_chain", description="All routes under this namespace concern hotel chain operations.")

hotel_chain_model = hotel_chain_namespace.model('HotelChain', {
    'chain_ID': fields.Integer(required=True, description='Hotel chain ID'),
    'name': fields.String(required=True, description='Hotel chain name'),
    'number_of_hotels': fields.Integer(required=True, description='Number of hotels in the chain')
})

hotel_chain_update_model = hotel_chain_namespace.model('HotelChainUpdate', {
    'chain_ID': fields.Integer(required=True, description='Hotel chain ID'),
    'name': fields.String(required=False, description='Hotel chain name'),
    'number_of_hotels': fields.Integer(required=False, description='Number of hotels in the chain')
})

@hotel_chain_namespace.route("/hotel_chain")
class HotelChain(Resource):
    @hotel_chain_namespace.doc(responses={200: "Success", 400: "Invalid input", 409: "Conflict", 500: "Internal Server Error"})
    def get(self):
        try:
            all_hotel_chains = current_app.db.get_all_hotel_chains()
            hotel_chains_json = []

            for hotel_chain in all_hotel_chains:
                hotel_chains_json.append({
                    'chain_ID': hotel_chain[0],
                    'name': hotel_chain[1],
                    'number_of_hotels': hotel_chain[2]
                })

            return hotel_chains_json, 200
        except Exception as e:
            return {"message": f"Error retrieving hotel chains: {e}"}, 500


    @hotel_chain_namespace.doc(responses={200: "Success", 400: "Invalid input", 409: "Conflict", 500: "Internal Server Error"})
    @hotel_chain_namespace.expect(hotel_chain_model)
    @jwt_required()
    def post(self):
        token_data = get_jwt()
        if not token_data.get("is_manager", False):
            return {"message": "Unauthorized!"}, 401

        data = request.json
        chain_id = data["chain_ID"]
        name = data["name"]
        number_of_hotels = data["number_of_hotels"]

        try:
            existing_hotel_chain = current_app.db.get_hotel_chain(chain_id, name)
            if existing_hotel_chain:
                return {"message": "Hotel chain with the given ID already exists."}, 409

            current_app.db.insert_hotel_chain(chain_id, name, number_of_hotels)
            return {"message": "Hotel chain added successfully."}, 201

        except Exception as e:
            return {"message": f"Error adding hotel chain: {e}"}, 500


    @hotel_chain_namespace.doc(responses={200: "Success", 400: "Invalid input", 401: "Unauthorized", 500: "Internal Server Error"})
    @hotel_chain_namespace.expect(hotel_chain_update_model)
    @jwt_required()
    def put(self):
        token_data = get_jwt()
        if not token_data.get("is_manager", False):
            return {"message": "Unauthorized!"}, 401

        data = request.json
        chain_id = data["chain_ID"]
        name = data.get("name")
        number_of_hotels = data.get("number_of_hotels")

        try:
            existing_hotel_chain = current_app.db.get_hotel_chain(chain_id)
            if not existing_hotel_chain:
                return {"message": "Hotel chain with the given ID does not exist."}, 404

            current_app.db.insert_hotel_chain(chain_id, name, number_of_hotels)
            return {"message": "Hotel chain updated successfully."}, 200

        except Exception as e:
            return {"message": f"Error updating hotel chain: {e}"}, 500


@hotel_chain_namespace.route("/hotel_chain/<int:chain_ID>")
class HotelChainByID(Resource):
    @hotel_chain_namespace.doc(responses={200: "Success", 404: "Not found", 500: "Internal Server Error"})
    def get(self, chain_ID):
        try:
            hotel_chain = current_app.db.get_hotel_chain(chain_ID)
            if not hotel_chain:
                return {"message": "Hotel chain not found."}, 404

            hotel_chain_json = {
                'chain_ID': hotel_chain[0],
                'name': hotel_chain[1],
                'number_of_hotels': hotel_chain[2]
            }
            return hotel_chain_json, 200

        except Exception as e:
            return {"message": f"Error retrieving hotel chain: {e}"}, 500

    @hotel_chain_namespace.doc(responses={200: "Success", 401: "Unauthorized", 404: "Not found", 500: "Internal Server Error"})
    @jwt_required()
    def delete(self, chain_ID):
        token_data = get_jwt()
        if not token_data.get("is_manager", False):
            return {"message": "Unauthorized!"}, 401

        try:
            existing_hotel_chain = current_app.db.get_hotel_chain(chain_ID)
            if not existing_hotel_chain:
                return {"message": "Hotel chain with the given ID does not exist."}, 404

            current_app.db.delete_hotel_chain(chain_ID)
            return {"message": "Hotel chain removed successfully."}, 200

        except Exception as e:
            return {"message": f"Error removing hotel chain: {e}"}, 500