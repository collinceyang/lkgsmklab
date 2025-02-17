#!/bin/bash
pwd
ls
rm -rf antenv  # Remove old virtual environment
python -m venv antenv  # Create new virtual environment
source antenv/bin/activate  # Activate virtual environment
python -m pip install --upgrade pip  # Upgrade pip
pip install -r requirements.txt  # Install dependencies
python --version
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4