import json
import time
import requests
from requests.auth import HTTPBasicAuth

timestamp1 =time.strftime("%Y%m%d%H%M%S", time.localtime())
print(timestamp1)

timestamp2 = int(timestamp1) + 1    
print(timestamp2)

amdgpuid = timestamp1
rocmid = str(timestamp2)

set_endpoint =  "set_ror"
url = f"http://localhost:80/{set_endpoint}/{amdgpuid}_{rocmid}"
print(url)
# response = requests.post(url)
response = requests.put(url)
if response.status_code == 200:
    json_str = json.dumps(response.json(), indent=4)
    print(f"response {url}:/n")
    print(json_str)
else:
    print("Error:", response.status_code, response.text)

get_endpoint =  "get_ror"
url = f"http://localhost:80/{get_endpoint}"

response = requests.get(url)
if response.status_code == 200:
    json_str = json.dumps(response.json(), indent=4)
    print(f"response {url}:/n")
    print(json_str)
    get_amdgpu_build = response.json()["amdgpu_build"]
    get_rocm_build = response.json()["rocm_build"]
    print(f"amdgpu_build: {get_amdgpu_build}")
    print(f"rocm_build: {get_rocm_build}")
    if get_amdgpu_build == amdgpuid and rocmid == get_rocm_build.split("/")[1]:
        print("Test set_ror passed")
    else:
        print("Test set_ror failed")
else:
    print("Error:", response.status_code, response.text)




