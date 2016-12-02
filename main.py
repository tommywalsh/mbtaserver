import database
import math
import public_api

# Code modified from the bisect module to allow searching based on a field
def bisect_left(array, value, key):
    lo = 0
    hi = len(array)
    while lo < hi:
        mid = (lo+hi)//2
        if array[mid][key] < value: lo = mid+1
        else: hi = mid
    return lo

def bisect_right(array, value, key):
    lo = 0
    hi = len(array)
    while lo < hi:
        mid = (lo+hi)//2
        if value < array[mid][key]: hi = mid
        else: lo = mid+1
    return lo

# For a sorted array, returns a slice of objects o such that min <= o[key] <= max
def get_subinterval(array, min, max, key):
    smallest = bisect_left(array, min, key)
    if smallest == len(array):
        return []

    largest = bisect_right(array, max, key)
    if not largest:
        return []

    return array[smallest:largest]

def get_ids(array):
    return frozenset(v['id'] for v in array)

# Returns all stops within the given distance from the given point
# For simplicity, this code searches a bounding square, not a circle.
def get_stops_near_location(db, lat, lon, radius):
    lat_rad = radius / 69 # 69 miles per degree
    lon_rad = radius / 51 # 51 miles per degree near Boston

    matching_lats =  get_ids(get_subinterval(db.stops_by_lat, lat - lat_rad, lat + lat_rad, 'lat'))
    matching_lons =  get_ids(get_subinterval(db.stops_by_lon, lon - lon_rad, lon + lon_rad, 'lon'))
    matching = matching_lats.intersection(matching_lons)
    stops = {}
    for id in matching:
        stops[id] = db.stops[id]
    return stops

# Returns distance in tenths of miles (about one large block)
def get_distance(lat1, lon1, lat2, lon2):
    dy = (lat2-lat1) * 690  # 69 miles per degree
    dx = (lon2-lon1) * 510  # 51 miles per degree near Boston
    return math.sqrt(dy*dy + dx*dx)

# For each route/direction in the given area, returns the outset closest to the given point
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
            outsets.append(public_api.make_outset(route_id, direction_id, best_outsets[route_id][direction_id]['stop_id']))
    return outsets
