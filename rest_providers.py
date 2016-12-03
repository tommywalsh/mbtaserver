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
