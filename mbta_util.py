import math
import bisector
import datatypes

# Various functions for processing MBTA data

def get_ids(array):
    return frozenset(v['id'] for v in array)

# Returns distance in tenths of miles (about one large block)
def get_distance(lat1, lon1, lat2, lon2):
    dy = (lat2-lat1) * 690  # 69 miles per degree
    dx = (lon2-lon1) * 510  # 51 miles per degree near Boston
    return math.sqrt(dy*dy + dx*dx)

# Returns all stops within the given distance from the given point
# For simplicity, this code searches a bounding square, not a circle.
def get_stops_near_location(db, lat, lon, radius):
    lat_rad = radius / 69 # 69 miles per degree
    lon_rad = radius / 51 # 51 miles per degree near Boston

    matching_lats =  get_ids(bisector.get_subinterval(db.stops_by_lat, lat - lat_rad, lat + lat_rad, 'lat'))
    matching_lons =  get_ids(bisector.get_subinterval(db.stops_by_lon, lon - lon_rad, lon + lon_rad, 'lon'))
    matching = matching_lats.intersection(matching_lons)
    stops = {}
    for id in matching:
        stops[id] = db.stops[id]
    return stops

def get_outsets_for_location(db, lat, lon, radius):
    best_outsets = {}
    stops = get_stops_near_location(db, lat, lon, radius)

    # This does a brute force O(n) search, assuming that the stop list is relatively small
    for stop in stops:
        stoplat = stops[stop]['lat']
        stoplon = stops[stop]['lon']
        distance = get_distance(lat, lon, stoplat, stoplon)
        for route in stops[stop]['routes']:
            route_id = route['route']
            direction_id = route['direction']
            if route_id not in best_outsets:
                best_outsets[route_id] = {}
            if direction_id not in best_outsets[route_id]:
                best_outsets[route_id][direction_id] = {}
            if distance not in best_outsets[route_id][direction_id] or best_outsets[route_id][direction_id]['distance'] > distance:
                best_outsets[route_id][direction_id]['distance'] = distance
                best_outsets[route_id][direction_id]['stop_id'] = stop

    # Finally, loop and create an array of actual Outset objects
    outsets = []
    for route_id in best_outsets:
        for direction_id in best_outsets[route_id]:
            outsets.append(datatypes.make_outset(route_id, direction_id, best_outsets[route_id][direction_id]['stop_id']))
    return outsets
