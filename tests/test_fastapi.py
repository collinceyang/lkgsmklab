import json
import time
import requests
from requests.auth import HTTPBasicAuth

end_points = ["get_hostname",
              "list_sut",
               "list_sku",
               "get_ror"]

for end_point in end_points:
    url = f"http://localhost:80/{end_point}"
    print("\n")
    response = requests.get(url)

    if response.status_code == 200:
        json_str = json.dumps(response.json(), indent=4)
        print(f"response {url}:")
        print(json_str)
    else:
        print("Error:", response.status_code, response.text)

end_point = "list_sku"
url = f"http://localhost:80/{end_point}"
print("\n")
response = requests.get(url)
if response.status_code == 200:
    sku_list = response.json()["sku_list"]
    print(sku_list)
    for sku in sku_list:
        url = f"http://localhost:80/get_sku_smk/{sku}"
        resp = requests.get(url)
        if resp.status_code == 200:
            json_str = json.dumps(resp.json(), indent=4)
            print(f"response {url}:")
            print(json_str)
        else:
            print("Error:", resp.status_code, resp.text)
else:
    print("Error:", response.status_code, response.text)

timestamp =time.strftime("%Y%m%d%H%M%S", time.localtime())
print(timestamp)


