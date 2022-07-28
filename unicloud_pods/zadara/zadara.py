from logs.setup_log import logger
from geopy.geocoders import Nominatim
import requests
import json
from .auth import Auth

class Zadara:
    def __init__(self, token):
        self.token = token
        self.pod = pod
        self.memories = []
        self.cpus = []
        self.vcores = []
        self.headers = {"Content-Type": "application/json"}
        self.allnodes = self.get_zadara_all_nodes(self.token)
        self.process = self.process()


    def get_zadara_all_nodes(self, token):
        token = token
        endpoint = '#/api/v2/nodes?detailed=true'
        try:
            self.headers['x-auth-token'] = token
            response = requests.get(f'{self.pod.url_base}{endpoint}', headers=self.headers, verify=False).json()
            return response
        except Exception as error:
            logger.error(error)
            return False

    def get_total_nodes(self):
        return len(self.allnodes) - self.pod.spare_nodes

    def get_total_memory(self):
        spare_memory = (sum(self.memories) / len(self.allnodes)) * self.pod.spare_nodes
        return ((sum(self.memories) - spare_memory) / (1024 ** 3)) * 0.9

    def get_total_total_fisical_cpu(self):
        return sum(self.cpus)

    def get_total_virtual_cores(self):
        return sum(self.vcores)*4

    def process(self):
        for node in self.allnodes:
            self.memories.append(node['total_memory_b'])
            self.cpus.append(len(node['cpus']))
            for cpu in node['cpus']:
                self.vcores.append(cpu['cores'])
        pass

    def get_pods_geolocation(self, location):
        try:
            geolocator = Nominatim(user_agent="Uni.Cloud")
            location = geolocator.geocode(location)
            return [location.longitude, location.latitude]
        except Exception as error:
            logger.error(error)
            return ['lon city wasnt found', 'lat city wasnt found']
