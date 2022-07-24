import requests
import json
from logs.setup_log import logger

class Auth:
    def __init__(self, pod):
        self.pod = pod
        self.first_auth_payload = {
            "auth": {
                "identity": {
                    "methods":
                        ["password"],
                    "password":
                        {"user":
                             {"name": pod.pod_user,
                              "password": pod.pod_password,
                              "domain": {"name": pod.domain_tenant
                                         }
                              }
                         }
                },
                "scope": {"domain": {"name": pod.domain_tenant}},
                "auto_enable_mfa": True}}
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
        self.url_base = f'{pod.url_base}'
        self.headers = {"Content-Type": "application/json"}

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