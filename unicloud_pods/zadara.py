from logs.setup_log import logger
from geopy.geocoders import Nominatim
import requests
import json

class Zadara:
    def __init__(self, pod):
        self.pod = pod
        self.url_base = f'{self.pod.url_base}'
        self.headers = {"Content-Type": "application/json"}
        self.first_auth_payload = {
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
        self.second_auth_payload = {
        "auth": {
            "identity": {
                "methods": [
                    "token"
                ],
                "token": {
                    "id": "token"
                }
            },
            "scope": {
                "project": {
                    "id": pod.project_id
                    }
                }
            }
        }

    def authentication(self):
        try:
            endpoint = "/api/v2/identity/auth"
            first_response = requests.post(f'{self.url_base}{endpoint}', data=json.dumps(self.first_auth_payload), headers=self.headers, verify=False)
            self.second_auth_payload['auth']['identity']['token']['id'] = first_response.headers['x-subject-token']

            second_response = requests.post(f'{self.url_base}{endpoint}', data=json.dumps(self.second_auth_payload), headers=self.headers, verify=False)
            return second_response.headers['x-subject-token']
        except Exception as error:
            logger.error(error)
            return error

    def get_zadara_pod_sparenodes(self):
        token = self.authentication()
        endpoint = '/api/v2/nodes?detailed=true'
        try:
            self.headers['x-auth-token'] = token
            all_nodes = requests.get(f'{self.url_base}{endpoint}', headers=self.headers, verify=False).json()
            qty_nodes = len(all_nodes)-self.pod.spare_nodes
            memory = []
            cpus = []
            vcores = []
            for node in all_nodes:
                memory.append(node['total_memory_b'])
                cpus.append(len(node['cpus']))
                for cpu in node['cpus']:
                    vcores.append(cpu['cores'])

            pod_memory = sum(memory)
            spare_memory = (pod_memory/len(all_nodes))*self.pod.spare_nodes
            total_memory = ((pod_memory-spare_memory)/(1024 ** 3))*0.9

            return [
                {'total_nodes': qty_nodes},
                {'total_memory': total_memory},
                {'total_fisical_cpu': sum(cpus)},
                {'total_vcores': sum(vcores)*4}
            ]
        except Exception as error:
            logger.error(error)
            return error

    def get_pods_geolocation(self, location):
        try:
            geolocator = Nominatim(user_agent="Uni.Cloud")
            location = geolocator.geocode(location)
            return [location.longitude, location.latitude]
        except Exception as error:
            logger.error(error)
            return ['lon city wasnt found', 'lat city wasnt found']

    # def get_total_memory(self):
    #     try:

