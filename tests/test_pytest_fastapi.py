import json
import pytest
import time
import requests
from requests.auth import HTTPBasicAuth



# function to get rest api response
def get_rest_api_response( base_url, end_point ):
    url = f"{base_url}/{end_point}"
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
def set_ror_api( base_url,timestamp1):
    timestamp2 = int(timestamp1) + 1    
    amdgpuid = timestamp1
    rocmid = str(timestamp2)
    set_endpoint =  "set_ror"
    url = f"{base_url}/{set_endpoint}/{amdgpuid}_{rocmid}"
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
def get_set_ror_api(base_url, timestamp1):
    timestamp2 = int(timestamp1) + 1    
    amdgpuid = timestamp1
    rocmid = str(timestamp2)
    get_endpoint =  "get_ror"
    set_ror_api(base_url,timestamp1) 
    url = f"{base_url}/{get_endpoint}"
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
@pytest.mark.smoke   
def test_request_timeout(request_timeout):
    assert print(f"Request Timeout = {request_timeout} sec") == True

@pytest.mark.smoke   
def test_user_password(env_username, env_password):
    assert print(f"Current User = {env_username} /Password = {env_password}") == True

@pytest.mark.api    
def test_get_hostname(api_base_url):
    assert get_rest_api_response(api_base_url,"get_hostname") == True

@pytest.mark.api 
def test_list_sut(api_base_url):
    assert get_rest_api_response(api_base_url,"list_sut") == True

@pytest.mark.api
def test_list_sku(api_base_url):
    assert get_rest_api_response(api_base_url,"list_sku") == True

@pytest.mark.api 
def test_get_ror(api_base_url):
    assert get_rest_api_response(api_base_url,"get_ror") == True

@pytest.mark.api 
def test_set_ror(api_base_url):
    timestamp1 =time.strftime("%Y%m%d%H%M%S", time.localtime())
    assert set_ror_api(api_base_url,timestamp1) == True

@pytest.mark.api 
def test_get_set_ror(api_base_url):
    timestamp1 =time.strftime("%Y%m%d%H%M%S", time.localtime())
    assert get_set_ror_api(api_base_url,timestamp1) == True

# def test_get_set_ror_fail():
#     time.sleep(3)
#     timestamp1 =time.strftime("%Y%m%d%H%M%S", time.localtime())
#     assert get_set_ror_api(timestamp1) == True  # Will be marked as failed but won't break the test run

@pytest.mark.xfail
def test_get_set_ror_xfail(api_base_url):
    time.sleep(3)
    timestamp1 =time.strftime("%Y%m%d%H%M%S", time.localtime())
    assert get_set_ror_api(api_base_url,timestamp1) == True  # Will be marked as failed but won't break the test run


