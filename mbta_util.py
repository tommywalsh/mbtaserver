import math
import bisector
import datatypes
import threader
import mbta_parser
from mbta_server import MBTAServer

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

server = MBTAServer()

def organize_outsets_by_stop(outsets):
    outsetsByStop = {}
    for outset in outsets:
        stop = outset['stop_id']
        if stop in outsetsByStop:
            outsetsByStop[stop].append(outset)
        else:
            outsetsByStop[stop] = [outset]
    return outsetsByStop

def get_tasks_for_stop_predictions(outsetsByStop):
    def make_getter(stop):
        def getter():
            return server.get_predictions_for_stop(stop)
        return getter

    tasks = []
    for stop in outsetsByStop:
        tasks.append(make_getter(stop))
    return tasks

def cull_predictions_for_outsets(predictions, outsetsByStop):
    culled_predictions = []
    for prediction in predictions:
        stop_id = prediction['stop_id']
        if stop_id in outsetsByStop:
            for outsetStop in outsetsByStop:
                for outset in outsetsByStop[outsetStop]:
                    if outset['route_id'] == prediction['route_id'] and outset['direction_id'] == prediction['direction_id']:
                        culled_predictions.append(prediction)
                        break
    return culled_predictions

def collect_predictions(outsetsByStop, results):
    all_predictions = []
    for result in results:
        predictions = mbta_parser.parse_stop_predictions(result)
        all_predictions.extend(cull_predictions_for_outsets(predictions, outsetsByStop))
    all_predictions.sort(key=lambda prediction: prediction['wait_time'])
    return all_predictions


def get_predictions_for_outsets(db, outsets):
    outsetsByStop = organize_outsets_by_stop(outsets)
    tasks = get_tasks_for_stop_predictions(outsetsByStop)
    (success, results) = threader.run_on_other_threads(tasks, 10)
    return collect_predictions(outsetsByStop, results)
