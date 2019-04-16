import requests

URL = "http://127.0.0.1:5000"

user_name = {"user_name" : "mlw60"}
r = requests.post(URL+'/new_user', json=user_name)
