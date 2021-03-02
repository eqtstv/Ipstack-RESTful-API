import requests
import sys

if __name__ == "__main__":
    if sys.argv[1] == "cloud":
        URL = "https://sofomo-assignment.herokuapp.com"

    if sys.argv[1] == "local":
        URL = "http://127.0.0.1:5000"


json = {"username": "testuser", "password": "longpassword"}

req = requests.post(f"{URL}/register", json=json)

print(req.text)
