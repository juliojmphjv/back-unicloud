from logs.setup_log import logger
from geopy.geocoders import Nominatim
import requests
import json

class Zadara:
    def __init__(self, pod):

        self.url_base = f'{pod.url_base}'
        self.headers = {"Content-Type": "application/json"}
        self.payload = {
        "auth":{
            "identity":{
                "methods":
                    ["password"],
                "password":
                    {"user":
                         {"name":pod.pod_user,
                          "password":pod.pod_password,
                          "domain":{"name":pod.domain_tenant
                                    }
                          }
                     }
            },
            "scope":{"domain":{"name":pod.domain_tenant}},
            "auto_enable_mfa":True}}

    def authenticate(self):
        endpoint = "/api/v2/identity/auth"
        response = requests.post(f'{self.url_base}{endpoint}', data=json.dumps(self.payload), headers=self.headers)
        return response.headers['x-subject-token']

    def get_zadara_pod_sparenodes(self):
        token = self.authenticate()
        endpoint = '/api/v2/nodes?detailed=true'
        try:
            self.headers['x-auth-token'] = token
            logger.info(self.headers)
            response = requests.get(f'{self.url_base}{endpoint}', headers=self.headers)
            logger.info(response.text)
        except Exception as error:
            logger.error(error)

        pass

    def get_pods_geolocation(self, location):
        try:
            geolocator = Nominatim(user_agent="Uni.Cloud")
            location = geolocator.geocode(location)
            return [location.longitude, location.latitude]
        except Exception as error:
            logger.error(error)
            return ['lon city wasnt found', 'lat city wasnt found']
