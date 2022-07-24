from geopy.geocoders import Nominatim
from logs.setup_log import logger

class GeoLocator:
    def __init__(self, location):
        self.__location = location

    def get_pods_geolocation(self):
        try:
            geolocator = Nominatim(user_agent="Uni.Cloud")
            location = geolocator.geocode(self.__location)
            return [location.longitude, location.latitude]
        except Exception as error:
            logger.error(error)
            return ['lon city wasnt found', 'lat city wasnt found']