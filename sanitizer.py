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
