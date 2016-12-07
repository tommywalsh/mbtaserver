import requests
import mbta_parser

# Note: secret.py is not checked into source control.
# It contains an API key for accessing the MBTA server.
# Each user of this code should provide their own file secret.py that defines
# API_KEY to be their own personal key.
import secret


# Code for making calls to the MBTA server
class MBTAServer:

    def run_get_request(self, url, params={}):
        params['api_key'] = secret.API_KEY
        params['format'] = 'json'
        result = requests.get(url, params=params)
        if result.status_code != 200:
            # We don't ever care why a server call failed, just that it failed.
            # So, just throw the same exception regardless of reason.
            raise ValueError ('Could not retrieve data for {}'.format(url))
        return result.json()

    def construct_url_for_endpoint(self, endpoint):
        return 'http://realtime.mbta.com/developer/api/v2/' + endpoint

    def get_all_routes(self):
        return mbta_parser.parse_routes(self.run_get_request(self.construct_url_for_endpoint('routes')))

    def get_stops_for_route(self, routeId):
        return mbta_parser.parse_stops(self.run_get_request(self.construct_url_for_endpoint('stopsbyroute'), {'route': routeId}), routeId)

    def get_predictions_for_stop(self, stopId):
        return self.run_get_request(self.construct_url_for_endpoint('predictionsbystop'), {'stop': stopId})
