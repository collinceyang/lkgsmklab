import json
import pytest
import time
import requests
from requests.auth import HTTPBasicAuth




# function to get rest api response with authentication
def get_rest_api_auth_response( base_url, end_point, headers ):
    url = f"{base_url}/{end_point}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json_str = json.dumps(response.json(), indent=4)
        print(f"response {url}:")
        print(json_str)
        return True
    else:
        print("Error:", response.status_code, response.text)
        return False

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


# function to set ror rest api with data file 
def set_ror_api_jsondata( base_url, json_data):  
    amdgpuid = json_data["amdgpu_build"]
    rocmid = json_data["rocm_build"]
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

# function to get/set rest api with json data
def get_ror_api_jsondata(base_url, json_data):
    amdgpuid = json_data["amdgpu_build"]
    rocmid = json_data["rocm_build"]
    get_endpoint =  "get_ror"
    url = f"{base_url}/{get_endpoint}"
    response = requests.get(url)
    if response.status_code == 200:
        # json_str = json.dumps(response.json(), indent=4)
        get_amdgpu_build = response.json()["amdgpu_build"]
        get_rocm_build = response.json()["rocm_build"]
        if get_amdgpu_build == amdgpuid and get_rocm_build.split("/")[1] == rocmid:
            # print("Test set_ror passed")
            return True
        else:
            # print("Test set_ror failed")
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
    print(f"Request Timeout = {request_timeout} sec")
    assert request_timeout is not None, "request_timeout should not be None"
    assert isinstance(request_timeout, (int, float)), "request_timeout should be a number"
    assert request_timeout > 0, "request_timeout should be greater than zero"

@pytest.mark.smoke   
def test_user_password(env_username, env_password):
    print(f"Current User = {env_username} /Password = {env_password}")
    assert env_username is not None, "env_username should not be None"
    assert env_password is not None, "env_password should not be None"
    assert isinstance(env_username, str), "env_username should be a string"
    assert isinstance(env_password, str), "env_password should be a string"
    assert len(env_username) > 0, "env_username should not be empty"
    assert len(env_password) > 0, "env_password should not be empty"

@pytest.mark.authapi
def test_api_auth_apikey_list_sut(api_base_url, request_api_headers):
    assert get_rest_api_auth_response(api_base_url,"v3/list_sut",request_api_headers) == True

@pytest.mark.authapi
def test_api_auth_token_list_sut(api_base_url, request_token_headers):
    assert get_rest_api_auth_response(api_base_url,"v2/list_sut",request_token_headers) == True

@pytest.mark.authapi
def test_api_no_auth_list_sut(api_base_url, request_default_headers):
    assert get_rest_api_auth_response(api_base_url,"list_sut",request_default_headers) == True

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

@pytest.mark.datadriven
def test_set_ror_jsondata(api_base_url, set_ror_data):
    assert set_ror_api_jsondata(api_base_url,set_ror_data) == True

@pytest.mark.datadriven
def test_get_ror_jsondata(api_base_url, set_ror_data):
    assert get_ror_api_jsondata(api_base_url,set_ror_data) == True


# def test_get_set_ror_fail():
#     time.sleep(3)
#     timestamp1 =time.strftime("%Y%m%d%H%M%S", time.localtime())
#     assert get_set_ror_api(timestamp1) == True  # Will be marked as failed but won't break the test run

@pytest.mark.xfail
def test_get_set_ror_xfail(api_base_url):
    time.sleep(3)
    timestamp1 =time.strftime("%Y%m%d%H%M%S", time.localtime())
    assert get_set_ror_api(api_base_url,timestamp1) == True  # Will be marked as failed but won't break the test run


