# Fast-Api-test-project-11.07.2022
test task

### activate venv (python3.10.5)
source env/bin/activate
### install libs from requirements.txt
env/bin/python3.10 -m pip install -r requirements.txt
### run fastapi APP on port: 8000
uvicorn app.main:app --port 8000 --reload
