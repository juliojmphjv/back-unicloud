from logs.setup_log import logger
from geopy.geocoders import Nominatim
import requests
import json

class Zadara:
    def __init__(self, pod):

        self.url_base = f'{pod.url_base}'
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
        url = self.url_base
        headers = {"Content-Type": "application/json"}
        response = requests.post(f'{url}/api/v2/identity/auth', data=json.dumps(self.payload), headers=headers)
        return response

    def get_zadara_pod_vcpu(self):

        pass

    def get_pods_geolocation(self, location):
        geolocator = Nominatim(user_agent="Uni.Cloud")
        location = geolocator.geocode(location)
        return [location.longitude, location.latitude]