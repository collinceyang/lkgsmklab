#!/bin/bash
source /home/site/wwwroot/antenv/bin/activate
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4