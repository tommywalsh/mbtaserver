import json
from mbta_server import MBTAServer

# An in-memory data store of various pieces of MBTA data that can be preloaded before any user queries

def read_json_file(filename):
    with open(filename) as file:
        return json.load(file)

class Database:
    def get_all_routes(self):
        return self.routes

    def get_all_stops(self):
        return self.stops

    def init_sorted_lat_stops(self):
        self.stops_by_lat = []
        for stop in self.stops:
            self.stops_by_lat.append({'id': stop, 'lat': self.stops[stop]['lat']})
        self.stops_by_lat.sort(key = lambda item: item['lat'])

    def init_sorted_lon_stops(self):
        self.stops_by_lon = []
        for stop in self.stops:
            self.stops_by_lon.append({'id': stop, 'lon': self.stops[stop]['lon']})
        self.stops_by_lon.sort(key = lambda item: item['lon'])

    def __init__(self, routes, stops):
        self.routes = routes
        self.stops = stops
        self.init_sorted_lat_stops()
        self.init_sorted_lon_stops()


def create_from_static_data():
    return Database(
        read_json_file('static_data/bus_routes.json'),
        read_json_file('static_data/bus_stops.json'))

def add_to_stops(stop_list, more_stops):
    for stop in more_stops:
        if stop in stop_list:
            stop_list[stop]['routes'].extend(more_stops[stop]['routes'])
        else:
            stop_list[stop] = more_stops[stop]

def create_from_mbta_server():
    server = MBTAServer();
    routes = server.get_all_routes()
    all_stops = {}
    for route in routes:
        route_stops = server.get_stops_for_route(route)
        add_to_stops(all_stops, route_stops)
    return Database(routes, all_stops)
