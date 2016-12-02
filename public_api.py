import main
import database
import json
from flask import Flask, request
from flask_restful import Resource, Api


def make_outset(route, direction, stop):
    return {
        'route_id': route,
        'direction_id': direction,
        'stop_id': stop
    }

class APIProvider:
    def __init__(self, database):
        self.db = database

    def get_outsets_for_location(self, lat, lon):
        return main.get_outsets_for_location(self.db, lat, lon, 0.25)

db = database.create_from_static_data()
provider = APIProvider(db)

class OutsetsForLocationREST(Resource):
    def post(self):
        # TODO: Do a safer deserialization here
        data = json.loads(request.data)
        outsets = provider.get_outsets_for_location(float(data['lat']), float(data['lon']))
        return outsets

app = Flask(__name__)
api = Api(app)

api.add_resource(OutsetsForLocationREST, '/outsetsForLocation')

if __name__ == '__main__':
    app.run(debug=True)
