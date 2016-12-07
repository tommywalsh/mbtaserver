import database
import sanitizer
import mbta_util

# Simple class that defines all of the public API functions.
# This code could just as well have been written inline in rest_providers, but it seemed cleaner
# to have this in one centralized place, if only for documentation purposes.
class APIProvider:
    def __init__(self, database):
        self.db = database

    def get_outsets_for_location(self, lat, lon):
        return mbta_util.get_outsets_for_location(self.db, lat, lon, 0.25)

    def get_predictions_for_outsets(self, outsets):
        return mbta_util.get_predictions_for_outsets(self.db, outsets)
