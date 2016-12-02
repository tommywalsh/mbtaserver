import json
from mbta_server import MBTAServer

def read_json_file(filename):
    with open(filename) as file:
        return json.load(file)

class Database:
    def get_all_routes(self):
        return self.routes

    def get_all_stops(self):
        return self.stops

def create_from_static_data():
    db = Database()
    db.routes = read_json_file('static_data/bus_routes.json')
    db.stops = read_json_file('static_data/bus_stops.json')
    return db

def add_to_stops(stop_list, more_stops):
    for stop in more_stops:
        if stop in stop_list:
            stop_list[stop]['routes'].extend(more_stops[stop]['routes'])
        else:
            stop_list[stop] = more_stops[stop]

def create_from_mbta_server():
    server = MBTAServer();
    db = Database()
    routes = server.get_all_routes()
    all_stops = {}
    for route in routes:
        route_stops = server.get_stops_for_route(route)
        add_to_stops(all_stops, route_stops)
    db.route = routes
    db.stops = all_stops
    return db
