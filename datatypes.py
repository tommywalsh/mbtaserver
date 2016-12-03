# Code for making object to be returned to user as part of the public API_KEY
def make_outset(route, direction, stop):
    return {
        'route_id': route,
        'direction_id': direction,
        'stop_id': stop
    }
