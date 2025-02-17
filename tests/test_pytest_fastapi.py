import json
import pytest
import time
import requests
from requests.auth import HTTPBasicAuth


# function to get rest api response
def get_rest_api_response(end_point):
    url = f"http://localhost:80/{end_point}"
    response = requests.get(url)
    if response.status_code == 200:
        json_str = json.dumps(response.json(), indent=4)
        print(f"response {url}:")
        print(json_str)
        return True
    else:
        print("Error:", response.status_code, response.text)
        return False


# function to set rest api response
def set_ror_api(timestamp1):
    timestamp2 = int(timestamp1) + 1    
    amdgpuid = timestamp1
    rocmid = str(timestamp2)
    set_endpoint =  "set_ror"
    url = f"http://localhost:80/{set_endpoint}/{amdgpuid}_{rocmid}"
    # print(url)
    # response = requests.post(url)
    response = requests.put(url)
    if response.status_code == 200:
        # json_str = json.dumps(response.json(), indent=4)
        # print(f"response {url}:/n")
        # print(json_str)
        return True
    else:
        print("Error:", response.status_code, response.text)
        return False

# function to get rest api response
def get_set_ror_api(timestamp1):    
    timestamp2 = int(timestamp1) + 1    
    amdgpuid = timestamp1
    rocmid = str(timestamp2)
    get_endpoint =  "get_ror"
    url = f"http://localhost:80/{get_endpoint}"
    response = requests.get(url)
    if response.status_code == 200:
        # json_str = json.dumps(response.json(), indent=4)
        get_amdgpu_build = response.json()["amdgpu_build"]
        get_rocm_build = response.json()["rocm_build"]
        if get_amdgpu_build == amdgpuid and  get_rocm_build.split("/")[1] == rocmid:
            # print("Test set_ror passed")
            return True
        else:
            # print("Test set_ror failed")
            return False



# Basic test case    
def test_get_hostname():
    assert get_rest_api_response("get_hostname") == True

def test_list_sut():
    assert get_rest_api_response("list_sut") == True

def test_list_sku():
    assert get_rest_api_response("list_sku") == True

def test_get_ror():
    assert get_rest_api_response("get_ror") == True

def test_set_ror():
    timestamp1 =time.strftime("%Y%m%d%H%M%S", time.localtime())
    assert set_ror_api(timestamp1) == True

def test_get_set_ror():
    timestamp1 =time.strftime("%Y%m%d%H%M%S", time.localtime())
    assert get_set_ror_api(timestamp1) == True

def test_get_set_ror_fail():
    time.sleep(3)
    timestamp1 =time.strftime("%Y%m%d%H%M%S", time.localtime())
    assert get_set_ror_api(timestamp1) == True  # Will be marked as failed but won't break the test run

@pytest.mark.xfail
def test_get_set_ror_xfail():
    time.sleep(3)
    timestamp1 =time.strftime("%Y%m%d%H%M%S", time.localtime())
    assert get_set_ror_api(timestamp1) == True  # Will be marked as failed but won't break the test run


