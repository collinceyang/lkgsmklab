import json
import time
import requests
from requests.auth import HTTPBasicAuth
from pymongo import MongoClient

timestamp1 =time.strftime("%Y%m%d%H%M%S", time.localtime())
print(timestamp1)

timestamp2 = int(timestamp1) + 1    
print(timestamp2)
amdgpuid = timestamp1
rocmid = str(timestamp2)

set_endpoint =  "set_ror"
url = f"http://localhost:8000/{set_endpoint}/{amdgpuid}_{rocmid}"
# print(url)
# response = requests.post(url) # support both post and put
response = requests.put(url)
if response.status_code == 200:
    json_str = json.dumps(response.json(), indent=4)
    print(f"response {url}:/n")
    print(json_str)
    test_result = True
    test_notes = "API set_ror passed"
else:
    print("Error:", response.status_code, response.text)
    test_result = False
    test_notes = "API set_ror failed"
# get host name
get_endpoint =  "get_hostname"
url = f"http://localhost:8000/{get_endpoint}"
response = requests.get(url)
if response.status_code == 200:
    json_str = json.dumps(response.json(), indent=4)
    print(f"response {url}:/n")
    print(json_str)
    test_result = True
    test_host = response.json()["host"]
else:
    print("Error:", response.status_code, response.text)
    test_result = False
    test_host = f"API {get_endpoint} failed"

#ingest result to MongoDB
# Extract relevant details
set_ror_details = {
    "TestCase": set_endpoint,
    "AmdgpuId": amdgpuid,
    "RocmId": rocmid,
    "Url": url,
    "Timestamp": timestamp1,
    "ApiResponse": response.text,
    "ApiStatusCode": response.status_code,
    "TestHost": test_host,
    "TestNotes": test_notes,
    "TestResult": test_result
}
# Connect to MongoDB (default host: localhost, port: 27017)
client = MongoClient("mongodb://localhost:27017/")
# Select (or create) a database
db = client["mongo_rest_api"]
# Select (or create) a collection (equivalent to a table in SQL)
collection = db["mongo_ror_collection"]
print("Connected to MongoDB!")
# Insert a single document
insert_result = collection.insert_one(set_ror_details)
print(f"Inserted document ID: {insert_result.inserted_id}")
client.close()

#validate if set ror properly 
get_os= "null"
get_gpu = "null"
get_amdgpu_path = "null"
get_endpoint =  "get_ror"
url = f"http://localhost:8000/{get_endpoint}"
response = requests.get(url)
if response.status_code == 200:
    json_str = json.dumps(response.json(), indent=4)
    print(f"response {url}:/n")
    print(json_str)
    get_amdgpu_build = response.json()["amdgpu_build"]
    get_rocm_build = response.json()["rocm_build"]
    print(f"amdgpu_build: {get_amdgpu_build}")
    print(f"rocm_build: {get_rocm_build}")
    get_os= response.json()["os"]
    get_gpu = response.json()["gpu"]
    get_amdgpu_path = response.json()["amdgpu"]
    if get_amdgpu_build == amdgpuid and rocmid == get_rocm_build.split("/")[1]:
        print("Test set_ror get_ror passed")
        test_result = True
        test_notes = "API set_ror and get_ror passed"
    else:
        print("Test set_ror pass and get_ror failed")
        test_result = False
        test_notes = "API set_ror pass and get_ror failed"
else:
    print("Error:", response.status_code, response.text)
    TestResult = False
# ingest result to MongoDB
# Extract relevant details
time.sleep(3)
timestamp1 =time.strftime("%Y%m%d%H%M%S", time.localtime())
get_ror_details = {
    "TestCase": get_endpoint,
    "AmdgpuId": get_amdgpu_build,
    "RocmId": get_rocm_build.split("/")[1],
    "OS": get_os,
    "GPU": get_gpu,
    "AMDGPUPath": get_amdgpu_path,
    "Url": url,
    "Timestamp": timestamp1,
    "ApiResponse": response.text,
    "ApiStatusCode": response.status_code,
    "TestHost": test_host,
    "TestNotes": test_notes,
    "TestResult": test_result
}
# Connect to MongoDB (default host: localhost, port: 27017)
client = MongoClient("mongodb://localhost:27017/")
# Select (or create) a database
db = client["mongo_rest_api"]
# Select (or create) a collection (equivalent to a table in SQL)
collection = db["mongo_ror_collection"]
print("Connected to MongoDB!")
# Insert a single document
insert_result = collection.insert_one(get_ror_details)
print(f"Inserted document ID: {insert_result.inserted_id}")
client.close()





















