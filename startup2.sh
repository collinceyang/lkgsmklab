#!/bin/bash
pwd
ls
python -m venv antenv
source /home/site/wwwroot/antenv/bin/activate
python -m pip install --upgrade pip
pip install setup
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4