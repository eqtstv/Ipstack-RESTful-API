import requests
import unittest

URL = "http://127.0.0.1:5000"


class TestRegister(unittest.TestCase):
    def test_no_json(self):
        # GIVEN
        # WHEN
        req = requests.post(f"{URL}/register").json()
        # THEN
        self.assertEqual("Missing JSON in request", req)

    def test_no_username(self):
        # GIVEN
        json = {"password": "longpassword"}
        # WHEN
        req = requests.post(f"{URL}/register", json=json).json()
        # THEN
        self.assertEqual("Wrong username or password parameter", req)

    def test_no_password(self):
        # GIVEN
        json = {"username": "testuser"}
        # WHEN
        req = requests.post(f"{URL}/register", json=json).json()
        # THEN
        self.assertEqual("Wrong username or password parameter", req)

    def test_user_exists(self):
        # GIVEN
        json = {"username": "testuser", "password": "longpassword"}
        # WHEN
        req = requests.post(f"{URL}/register", json=json).json()
        # THEN
        self.assertEqual("User aleady exists", req)


class TestLogin(unittest.TestCase):
    def test_no_json(self):
        # GIVEN
        # WHEN
        req = requests.post(f"{URL}/login").json()
        # THEN
        self.assertEqual("Missing JSON in request", req)

    def test_no_username(self):
        # GIVEN
        json = {"password": "longpassword"}
        # WHEN
        req = requests.post(f"{URL}/login", json=json).json()
        # THEN
        self.assertEqual("Wrong username or password parameter", req)

    def test_no_password(self):
        # GIVEN
        json = {"username": "testuser"}
        # WHEN
        req = requests.post(f"{URL}/login", json=json).json()
        # THEN
        self.assertEqual("Wrong username or password parameter", req)

    def test_wrong_username_password_combination(self):
        # GIVEN
        json = {"username": "testuser", "password": "wrongpassword"}
        # WHEN
        req = requests.post(f"{URL}/login", json=json).json()
        # THEN
        self.assertEqual("Wrong username and password combination", req)

    def test_valid_username_password_combination(self):
        # GIVEN
        json = {"username": "testuser", "password": "longpassword"}
        # WHEN
        req = requests.post(f"{URL}/login", json=json).json()
        # THEN
        self.assertIn("access_token", req)


class TestLocationPOST(unittest.TestCase):
    def test_no_access_token(self):
        # GIVEN
        json = {"address": "www.google.com"}
        # WHEN
        req = requests.post(f"{URL}/location", json=json).json()
        # THEN
        self.assertEqual({"msg": "Missing Authorization Header"}, req)

    def test_no_json(self):
        # GIVEN
        json = {"username": "testuser", "password": "longpassword"}
        req = requests.post(f"{URL}/login", json=json).json()
        auth_token = req["access_token"]
        # WHEN
        req = requests.post(
            f"{URL}/location", headers={"Authorization": f"Bearer {auth_token}"}
        ).json()
        # THEN
        self.assertEqual("Missing JSON in request", req)

    def test_wrong_json(self):
        # GIVEN
        json = {"username": "testuser", "password": "longpassword"}
        req = requests.post(f"{URL}/login", json=json).json()
        auth_token = req["access_token"]
        json = {"addresssss": "www.google.com"}
        # WHEN
        req = requests.post(
            f"{URL}/location",
            json=json,
            headers={"Authorization": f"Bearer {auth_token}"},
        ).json()
        # THEN
        self.assertEqual("Wrong json", req)

    def test_wrong_address(self):
        # GIVEN
        json = {"username": "testuser", "password": "longpassword"}
        req = requests.post(f"{URL}/login", json=json).json()
        auth_token = req["access_token"]
        json = {"address": "not-internet-address"}
        # WHEN
        req = requests.post(
            f"{URL}/location",
            json=json,
            headers={"Authorization": f"Bearer {auth_token}"},
        ).json()
        # THEN
        self.assertEqual("Wrong address", req)

    def test_address_already_in_the_database(self):
        # GIVEN
        json = {"username": "testuser", "password": "longpassword"}
        req = requests.post(f"{URL}/login", json=json).json()
        auth_token = req["access_token"]
        json = {"address": "www.google.com"}
        # WHEN
        req = requests.post(
            f"{URL}/location",
            json=json,
            headers={"Authorization": f"Bearer {auth_token}"},
        ).json()
        # THEN
        self.assertEqual("Address already in the database", req)


class TestLocationDELETE(unittest.TestCase):
    def test_no_access_token(self):
        # GIVEN
        json = {"address": "www.google.com"}
        # WHEN
        req = requests.post(f"{URL}/location", json=json).json()
        # THEN
        self.assertEqual({"msg": "Missing Authorization Header"}, req)

    def test_no_json(self):
        # GIVEN
        json = {"username": "testuser", "password": "longpassword"}
        req = requests.post(f"{URL}/login", json=json).json()
        auth_token = req["access_token"]
        # WHEN
        req = requests.post(
            f"{URL}/location", headers={"Authorization": f"Bearer {auth_token}"}
        ).json()
        # THEN
        self.assertEqual("Missing JSON in request", req)

    def test_wrong_json(self):
        # GIVEN
        json = {"username": "testuser", "password": "longpassword"}
        req = requests.post(f"{URL}/login", json=json).json()
        auth_token = req["access_token"]
        json = {"addresssss": "www.google.com"}
        # WHEN
        req = requests.post(
            f"{URL}/location",
            json=json,
            headers={"Authorization": f"Bearer {auth_token}"},
        ).json()
        # THEN
        self.assertEqual("Wrong json", req)

    def test_wrong_address(self):
        # GIVEN
        json = {"username": "testuser", "password": "longpassword"}
        req = requests.post(f"{URL}/login", json=json).json()
        auth_token = req["access_token"]
        json = {"address": "not-internet-address"}
        # WHEN
        req = requests.post(
            f"{URL}/location",
            json=json,
            headers={"Authorization": f"Bearer {auth_token}"},
        ).json()
        # THEN
        self.assertEqual("Wrong address", req)

    def test_address_already_in_the_database(self):
        # GIVEN
        json = {"username": "testuser", "password": "longpassword"}
        req = requests.post(f"{URL}/login", json=json).json()
        auth_token = req["access_token"]
        json = {"address": "www.google.com"}
        # WHEN
        req = requests.post(
            f"{URL}/location",
            json=json,
            headers={"Authorization": f"Bearer {auth_token}"},
        ).json()
        # THEN
        self.assertEqual("Address already in the database", req)


class TestLocationGET(unittest.TestCase):
    def test_address_not_in_the_database(self):
        # GIVEN
        json = {"username": "testuser", "password": "longpassword"}
        req = requests.post(f"{URL}/login", json=json).json()
        auth_token = req["access_token"]
        json = {"address": "www.addressnotindb.com"}
        # WHEN
        req = requests.get(
            f"{URL}/location",
            json=json,
            headers={"Authorization": f"Bearer {auth_token}"},
        ).json()
        # THEN
        self.assertEqual("Address not in the database", req)

    def test_address_in_the_database(self):
        # GIVEN
        json = {"username": "testuser", "password": "longpassword"}
        req = requests.post(f"{URL}/login", json=json).json()
        auth_token = req["access_token"]
        json = {"address": "www.google.com"}
        # WHEN
        req = requests.get(
            f"{URL}/location",
            json=json,
            headers={"Authorization": f"Bearer {auth_token}"},
        ).json()
        # THEN
        valid_dict = {
            "address": "www.google.com",
            "ip": "2607:f8b0:4004:808::2004",
            "type": "ipv6",
            "continent_code": "NA",
            "continent_name": "North America",
            "country_code": "US",
            "country_name": "United States",
            "region_code": "VA",
            "region_name": "Virginia",
            "city": "Herndon",
            "zip": "22095",
            "latitude": 38.98371887207031,
            "longitude": -77.38275909423828,
        }
        self.assertEqual(valid_dict, req)
