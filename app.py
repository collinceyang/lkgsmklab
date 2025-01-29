import json
import os
import socket
import time
from datetime import datetime, timezone
from typing import Dict
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request



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

hostname = socket.gethostname()
expected_postcode = "200,201,202,203"

#####
# host config
#####

####
load_dotenv()
artifactory_auth = os.getenv('artifactory_auth')
sut_key = os.getenv('sut_key')
sdu_passwd = os.getenv('sdu_passwd')
web_user = os.getenv('web_user')
web_passwd = os.getenv('web_passwd')
pikvm_auth = os.getenv('pikvm_auth')
####
app = FastAPI()
templates = Jinja2Templates(directory="templates")

security = HTTPBasic()
fake_db: Dict[str, str] = {
    web_user: web_passwd
}

@app.get("/", response_class=HTMLResponse)
async def read_root_credential(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = fake_db.get(credentials.username)
    if correct_username is None or correct_username != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return templates.TemplateResponse("lab.html", {"request": request, "lab_data": data_lab})

#response list of sut_name
@app.get("/list_sut")
def get_sut_list():
    sut_list = []
    sut_list_dict = {}
    for each in data_lab:
        sut_list.append(each["sut_name"])
    sut_list_dict["sut_list"] = sut_list
    print(sut_list)
    print(sut_list_dict)
    return sut_list_dict

@app.get("/list_sku")
def get_sku_list():
    sku_list = []
    sku_list_dict = {}
    for each in data_lkg:
        sku_list.append(each["sku"])
    sku_list_dict["sku_list"] = sku_list
    print(sku_list)
    print(sku_list_dict)
    return sku_list_dict

@app.get("/get_ror")
def get_ror_lkg():
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
async def set_ror(amdgpuid_rocmid: str):
    amdgpu_id, rocm_id = amdgpuid_rocmid.split("_")
    print(f'amdgpu_id is set to {amdgpu_id}')
    print(f'rocm_id is set to {rocm_id}')
    data_ror["amdgpu_build"] = amdgpu_id
    data_ror["rocm_build"] = f"compute-rocm/{rocm_id}"
    return {"message": f"ROR LKG version set to {amdgpu_id} and {rocm_id}"}

#response set of lkg of navi GPU by SKU
@app.post("/set_sku_lkg/{sku}/{ifwi_path}")
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

