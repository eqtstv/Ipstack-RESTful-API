import requests
import sys

if __name__ == "__main__":
    if sys.argv[1] == "cloud":
        URL = "https://sofomo-assignment.herokuapp.com"

    if sys.argv[1] == "local":
        URL = "http://127.0.0.1:5000"

json = {"username": "testuser", "password": "longpassword"}

req = requests.post(f"{URL}/login", json=json).json()

if "access_token" in req:
    auth_token = req["access_token"]
else:
    print(req)


json = {"address": "www.olx.pl"}

req = requests.post(
    f"{URL}/location",
    json=json,
    headers={"Authorization": f"Bearer {auth_token}"},
).json()

print(req)

req1 = requests.get(
    f"{URL}/location",
    json=json,
    headers={"Authorization": f"Bearer {auth_token}"},
).json()

print(req1)