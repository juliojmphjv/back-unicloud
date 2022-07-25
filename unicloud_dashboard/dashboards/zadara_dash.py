from unicloud_dashboard.interfaces.dashboard import DashboardInterface
from unicloud_pods.zadara.auth_payloads import AuthPayload
import requests
import json
from logs.setup_log import logger
from unicloud_pods.zadara.auth import Auth
from unicloud_pods.models import ZadaraPods
from unicloud_customers.models import Customer
from .pod_geolocation import GeoLocator

class ZadaraDashboard(DashboardInterface):

    def __init__(self, pod, organization) -> None:
        self.pod = pod
        self.organization = organization
        self.headers = {"Content-Type": "application/json"}
        self.dashboard = {
            'pod_name': '',
            'total_spare_nodes': 0,
            'total_nodes': 0,
            'total_memory': 0,
            'total_physical_cpu': 0,
            'total_vcores': 0,
            'location': [],
        }
        self.cpus = []
        self.memories = []
        self.vcores = []
        self.pod_token = self.__generate_token()
        self.allnodes = self.__get_zadara_all_nodes()
        self.process = self.__cpu_mem_data_process()


    def __generate_token(self) -> str:
        authenticator = Auth(self.pod)

        return authenticator.authentication()

    def __get_zadara_all_nodes(self):
        endpoint = '/api/v2/nodes?detailed=true'
        try:
            self.headers['x-auth-token'] = self.pod_token
            response = requests.get(f'{self.pod.url_base}{endpoint}', headers=self.headers, verify=False).json()
            return response
        except Exception as error:
            logger.error(error)
            return False

    def __get_total_nodes(self) -> int:
        return len(self.__get_zadara_all_nodes()) - self.pod.spare_nodes

    def __get_total_memory(self) -> int:
        spare_memory = (sum(self.memories) / len(self.allnodes)) * self.pod.spare_nodes
        return ((sum(self.memories) - spare_memory) / (1024 ** 3)) * 0.9

    def __cpu_mem_data_process(self):
        for node in self.allnodes:
            self.memories.append(node['total_memory_b'])
            self.cpus.append(len(node['cpus']))
            for cpu in node['cpus']:
                self.vcores.append(cpu['cores'])
        pass

    def __get_total_total_fisical_cpu(self) -> int:
        return sum(self.cpus)

    def __get_total_virtual_cores(self) -> int:
        return sum(self.vcores)*4

    def get_dashboard(self):
        try:
            geolocator = GeoLocator(self.pod.location)
            self.dashboard['location'].append({self.pod.location: geolocator.get_pods_geolocation()})
        except Exception as error:
            logger.error(error)
        self.dashboard['total_spare_nodes'] = self.pod.spare_nodes
        self.dashboard['total_nodes'] = self.__get_total_nodes()
        self.dashboard['total_memory'] = self.__get_total_memory()
        self.dashboard['total_physical_cpu'] = self.__get_total_total_fisical_cpu()
        self.dashboard['total_vcores'] = self.__get_total_virtual_cores()
        self.dashboard['pod_name'] = self.pod.name

        return self.dashboard

