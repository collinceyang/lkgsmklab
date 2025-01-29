# lkgsmklab
# restful api to provide lkg smoke stack info

cd ~/lkgsmklab
python3 -m venv ~/lkgsmklab

#activate venv 
source bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 80 --reload

#Access the Application
#Open your browser and go to http://127.0.0.1:80/docs to see the dynamic HTML generated from the JSON data.

