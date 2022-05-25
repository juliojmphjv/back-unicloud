import requests
import json
import base64

def zadara_login():
    payload = {
        "auth":{
            "identity":{
                "methods":
                    ["password"],
                "password":
                    {"user":
                         {"name":"unicloud.broker",
                          "password":"1234@UniIT",
                          "domain":{"name":"cloud_msp"}
                          }
                     }
            },
            "scope":{"domain":{"name":"cloud_msp"}},
            "auto_enable_mfa":True}}


    usuario = 'unicloud.broker'
    senha = '1234@UniIT'
    url = 'https://br01-console.uni.cloud/api/v2/identity/auth'
    headers = {"Content-Type":"application/json"}

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    json_data = json.dumps(response.text)

    encoded = json_data.encode()
    b64encode = base64.b64encode(encoded)
    print(str(b64encode))

    volumeheader = {"Content-Type" : "application/json", "x-auth-token": str(b64encode)}
    volume = 'https://br01-console.uni.cloud/api/v2/volumes'

    volume = requests.get(volume, headers=volumeheader)

    print(volume.text)


zadara_login()