import requests
import secret

class MBTAServer:

    def runGetRequest(self, url, params={}):
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
        return self.runGetRequest(self.construct_url_for_endpoint('routes'))


server = MBTAServer()
print server.get_all_routes()