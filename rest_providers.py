import sanitizer
import database
import public_api
from flask_restful import Resource
from flask import request

# This code containser endpoint providers for all of our REST calls

# All calls go through the APIProvider
db = database.create_from_static_data()
provider = public_api.APIProvider(db)

class OutsetsForLocation(Resource):
    def post(self):
        lat, lon = sanitizer.parse_lat_lon(request.data)
        outsets = provider.get_outsets_for_location(lat, lon)
        return outsets

class DeparturesForOutsets(Resource):
    def post(self):
        outsets = sanitizer.parse_outsets(db, request.data)
        return provider.get_predictions_for_outsets(outsets)

outsets = [
    {"stop_id": "2615", "route_id": "86", "direction_id": "1"},
    {"stop_id": "25712", "route_id": "86", "direction_id": "0"},
    {"stop_id": "2510", "route_id": "87", "direction_id": "1"},
    {"stop_id": "2531", "route_id": "91", "direction_id": "0"},
    {"stop_id": "2511", "route_id": "91", "direction_id": "1"},
    {"stop_id": "2511", "route_id": "85", "direction_id": "1"},
]

#provider.get_predictions_for_outsets(outsets)
