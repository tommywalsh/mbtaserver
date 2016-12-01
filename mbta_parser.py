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
