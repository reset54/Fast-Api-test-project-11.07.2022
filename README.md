# Fast-Api-test-project-11.07.2022
test task

### activate venv ([python3.10.5](https://github.com/reset54/instructions_54/blob/main/python3.10.5_on_debian_installer.sh "установка Python3.10.5"))
source env/bin/activate
### install libs from requirements.txt
env/bin/python3.10 -m pip install -r requirements.txt
### run fastapi APP on port: 8000
uvicorn app.main:app --port 8000 --reload

![image](https://user-images.githubusercontent.com/40237958/178517135-80842748-2266-4e26-87b6-951f3557921a.png)
