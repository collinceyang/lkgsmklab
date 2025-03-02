import json
import os
import socket
import time
from datetime import datetime, timezone
from typing import Dict
from typing import Optional
import requests
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader
from fastapi.security import  OAuth2PasswordBearer

# Define API key authentication
API_KEY = "my_secure_api_key"  # Store securely (e.g., environment variable)
API_KEY_NAME = "X-API-Key"
###
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
def get_api_key(api_key: str = Depends(api_key_header)):
    """Validate API Key"""
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key

# Define OAuth2  authentication
VALID_BEARER_TOKENS = ["valid_oauth_token_example"]  # Store and validate in DB or token service
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # OAuth2 Bearer Token

# Authentication function that allows either API Key or Bearer Token
def authenticate(
    api_key: Optional[str] = Security(api_key_header),
    token: Optional[str] = Security(oauth2_scheme)
):
    print(f"Received API Key: {api_key}")  # Debugging
    print(f"Received Token: {token}")      # Debugging
    if api_key:
        print(f"API Key Provided: {api_key}")
    if token:
        print(f"Bearer Token Provided: {token}")
    if api_key == API_KEY:
        return {"auth_method": "API Key", "user": "api_user"}
    elif token in VALID_BEARER_TOKENS:
        return {"auth_method": "OAuth2 Bearer", "user": "oauth_user"}
    else:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")



# Load JSON data for navi lab
with open("lab_navi.json") as f:
    data_lab = json.load(f)
# Load JSON data for lkg navi ifwi
with open("lkg_navi_ifwi.json") as f_lkg:
    data_lkg = json.load(f_lkg)
# Load JSON data for lkg navi ifwi
with open("smk_navi_ifwi.json") as smk_f:
    data_smk = json.load(smk_f)
# Load JSON data for lkg ror
with open("lkg_ror.json") as ror_lkg:
    data_ror = json.load(ror_lkg)


expected_postcode = "200,201,202,203"

#####
# host config
#####

####

####
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# V3 (API Key Authentication Required)
@app.get("/v3/list_sut", dependencies=[Depends(get_api_key)])
async def get_sut_list_v3():
    sut_list = [each["sut_name"] for each in data_lab]
    return {"auth_info": "api-key" ,"sut_list": sut_list, "from_host": socket.gethostname(), "version": "v3 (api key Authenticated)"}

# V2 (OAuth Key Token Authentication Required)
@app.get("/v2/list_sut")
def get_sut_list(auth_info: dict = Depends(authenticate)):
    sut_list = [each["sut_name"] for each in data_lab]
    return { "auth_info": auth_info,"sut_list": sut_list, "from_host": socket.gethostname(), "version": "v2 (token Authenticated)"}


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("lab.html", {"request": request, "lab_data": data_lab})

#response current hostname
@app.get("/get_hostname")
def get_hostname():
    hostname = socket.gethostname()
    print(hostname)
    hostname_dict = {"host":hostname}
    return hostname_dict

#response list of sut_name
@app.get("/list_sut")
def get_sut_list():
    sut_list = []
    sut_list_dict = {}
    for each in data_lab:
        sut_list.append(each["sut_name"])
    sut_list_dict["sut_list"] = sut_list
    sut_list_dict["from_host"] = socket.gethostname()
    print(sut_list_dict)
    return sut_list_dict

@app.get("/list_sku")
def get_sku_list():
    sku_list = []
    sku_list_dict = {}
    for each in data_lkg:
        sku_list.append(each["sku"])
    sku_list_dict["sku_list"] = sku_list
    sku_list_dict["from_host"] = socket.gethostname()
    print(sku_list_dict)
    return sku_list_dict

@app.get("/get_ror")
def get_ror_lkg():
    data_ror["from_host"] = socket.gethostname()
    print(data_ror)
    return data_ror

#response dump snapshot of current json data base
@app.get("/dump_data")
def get_data_snapshot():
    now = datetime.now(timezone.utc)
    datestring = now.strftime("%Y%m%d%H")
    print("Dump Lkg Data as json file")
    file_path = f"dump_lkg_navi_ifwi_{datestring}.json"
    with open(file_path, "w", encoding="utf-8") as file:
        print(f"\nCreating {file_path}\n")
        json.dump(data_lkg, file)
    print("Dump Smk Data as json file")
    file_path = f"dump_smk_navi_ifwi_{datestring}.json"
    with open(file_path, "w", encoding="utf-8") as file:
        print(f"\nCreating {file_path}\n")
        json.dump(data_smk, file)
    print("Dump RoR Data as json file")
    file_path = f"dump_lkg_ror_{datestring}.json"
    with open(file_path, "w", encoding="utf-8") as file:
        print(f"\nCreating {file_path}\n")
        json.dump(data_ror, file)
    print("Dump Lab Data as json file")
    file_path = f"dump_lab_navi_{datestring}.json"
    with open(file_path, "w", encoding="utf-8") as file:
        print(f"\nCreating {file_path}\n")
        json.dump(data_lab, file)
    return {"message": "Dump data as json files!!! "}

#response indicated sku firmware info
@app.get("/get_sku_lkg/{sku}")
def get_skulkg_json(sku: str):
    try:
        for each in data_lkg:
            if each["sku"] == sku:
                print(f"find json data of {sku}!!!")
                each["from_host"] = socket.gethostname()
                print(each)
                return each
            else:
                response_json = 'null'
        return response_json
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail=repr(e))

#response indicated sku smoke info
@app.get("/get_sku_smk/{sku}")
def get_skusmk_json(sku: str):
    try:
        for each in data_smk:
            if each["sku"] == sku:
                print(f"find json data of {sku}!!!")
                each["from_host"] = socket.gethostname()
                print(each)
                return each
            else:
                response_json = 'null'
        return response_json
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail=repr(e))

#response indicated sut_name json info
@app.get("/get_sut/{sut_name}")
def get_sut_json(sut_name: str):
    try:
        for each in data_lab:
            if each["sut_name"] == sut_name:
                print(f"find json data of {sut_name}!!!")
                each["from_host"] = socket.gethostname()
                print(each)
                return each
            else:
                response_json = 'null'
        return response_json
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail=repr(e))

#response set of lkg of ror
@app.post("/set_ror/{amdgpuid_rocmid}")
@app.put("/set_ror/{amdgpuid_rocmid}")
async def set_ror(amdgpuid_rocmid: str):
    amdgpu_id, rocm_id = amdgpuid_rocmid.split("_")
    print(f'amdgpu_id is set to {amdgpu_id}')
    print(f'rocm_id is set to {rocm_id}')
    data_ror["amdgpu_build"] = amdgpu_id
    data_ror["rocm_build"] = f"compute-rocm/{rocm_id}"
    return {"message": f"ROR LKG version set to {amdgpu_id} and {rocm_id}"}

#response set of lkg of navi GPU by SKU
@app.post("/set_sku_lkg/{sku}/{ifwi_path}")
@app.put("/set_sku_lkg/{sku}/{ifwi_path}")
async def set_sku_lkg(sku: str, ifwi_path: str):
    for each in data_lkg:
        if sku == each["sku"]:
            each["firmware_path"] = ifwi_path
            break
        else:
            print("Invalid SKU!!!")
    file_path = "lkg_navi_ifwi.json"
    with open(file_path, "w", encoding="utf-8") as file:
        print(f"\nWriting {file_path}\n")
        json.dump(data_lkg, file)
    return {"message": f"set LKG stack to {ifwi_path} for {sku}"}

#response set of smk of navi GPU by SKU
@app.post("/set_sku_smk/{sku}/{ifwi_path}")
@app.put("/set_sku_smk/{sku}/{ifwi_path}")
async def set_sku_smk(sku: str, ifwi_path: str):
    for each in data_lkg:
        if sku == each["sku"]:
            each["firmware_path"] = ifwi_path
            break
        else:
            print("Invalid SKU!!!")
    file_path = "smk_navi_ifwi.json"
    with open(file_path, "w", encoding="utf-8") as file:
        print(f"\nWriting {file_path}\n")
        json.dump(data_lkg, file)
    return {"message": f"set Smoke stack to {ifwi_path} for {sku}"}

