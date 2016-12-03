# This code handles translation from the data returned by the MBTA's server into a format more useful to us.

def get_value(json, key):
    if key in json:
        return json[key]
    raise ValueError('Unexpected JSON format: no field {} in {}'.format(key, json))

def parse_routes(json):
    all_routes = {}
    modes = get_value(json, 'mode')
    for mode in modes:
        routes = get_value(mode, 'route')
        for route in routes:
            route_id = route['route_id']
            route_name = route['route_name']
            all_routes[route_id] = {
                'name' : route_name,
            }
    return all_routes

def has_value(object, name):
    return name in object and object[name]

def parse_stops(json, route_id):
    all_stops = {}
    directions = get_value(json, 'direction')
    for direction in directions:
        direction_id = get_value(direction, 'direction_id')
        stops = get_value(direction, 'stop')
        for stop in stops:
            stop_id = get_value(stop, 'stop_id')
            rd = {'route': route_id, 'direction': direction_id}
            if stop_id in all_stops:
                all_stops[stop_id]['routes'].append(rd)
            else:
                stop_info = {
                    'stop_name' : get_value(stop, 'stop_name'),
                    'lat' : float(get_value(stop, 'stop_lat')),
                    'lon' : float(get_value(stop, 'stop_lon')),
                    'routes' : [rd]
                }
                if has_value(stop, 'parent_station_name'):
                    stop_info['parent_station_name'] = stop['parent_station_name']
                all_stops[stop_id] = stop_info
    return all_stops
