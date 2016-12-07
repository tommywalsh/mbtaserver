import json

# This code "sanitizes" input received from the user, guaranteeing that it is
# in a format that the rest of the code can handle without any security issues

def parse_float(data, field):
    if field in data:
        return float(data[field])
    raise ValueError('Field {} not supplied'.format(field))

def parse_latitude(data):
    lat = parse_float(data, 'lat')
    if lat < 41 or lat > 43:
        raise ValueError('Latitude out of range')
    return lat

def parse_longitude(data):
    lon = parse_float(data, 'lon')
    if lon < -72 or lon > -70:
        raise ValueError('Longitude out of range')
    return lon

def json_to_object(jsonString):
    return json.loads(jsonString)

def parse_lat_lon(jsonString):
    data = json_to_object(jsonString)
    return parse_latitude(data), parse_longitude(data)

def validated_outset(db, outset):
    if 'route_id' in outset and 'direction_id' in outset and 'stop_id' in outset:
        if outset['route_id'] in db.get_all_routes() and outset['stop_id'] in db.get_all_stops():
            if outset['direction_id'] in ['0', '1']:
                return {
                    'route_id': outset['route_id'],
                    'stop_id': outset['stop_id'],
                    'direction_id': outset['direction_id']
                }
    raise ValueError('Unrecognized input format')

def parse_outsets(db, jsonString):
    data = json_to_object(jsonString)
    if not isinstance(data, list):
        raise ValueError('Input must be an array')
    outsets = []
    for outset in data:
        outsets.append(validated_outset(db, outset))
    return data
