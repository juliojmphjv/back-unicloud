
class AuthPayload:
    def __init__(self, pod):
        self.__first_auth_payload = {
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

        self.__second_auth_payload = {
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

    def get_payloads(self):
        return {'first_auth_payload': self.__first_auth_payload, 'second_auth_payload': self.__second_auth_payload}