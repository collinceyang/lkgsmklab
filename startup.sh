#!/bin/bash
pwd
ls
source /home/site/wwwroot/antenv/bin/activate
uvicorn app:app --host 0.0.0.0 --port 80 --workers 4