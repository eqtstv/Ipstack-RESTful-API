# sofomo-assignment

https://sofomo-assignment.herokuapp.com/

docker build --no-cache -t sofomo-assignment:latest .
docker run -dp 5000:5000 sofomo-assignment

## API routes

### Register

url: `/register`

method: `POST`

json format:

```json
{ "username": "exampleuser", "password": "examplepassword" }
```

example request:

```python
requests.post("https://sofomo-assignment.herokuapp.com/register",
     json={"username": "exampleuser", "password": "examplepassword"}).json()
```

returns:

- `User created`

OR

- `Wrong username or password paramenter`

OR

- `User already exists`

OR

- `Missing JSON in request`

### Login

url: `/login`

method: `POST`

json format:

```json
{ "username": "exampleuser", "password": "examplepassword" }
```

example request:

```python
requests.post("https://sofomo-assignment.herokuapp.com/login",
     json={"username": "exampleuser", "password": "examplepassword"}).json()
```

returns:

- ```json
  {
    "access_token": "user_access_token"
  }
  ```

OR

- `Wrong username or password paramenter`

OR

- `Wrong username and password combination`

OR

- `Missing JSON in request`

### Location

Protected by JWT

```python
json = {"username": "testuser", "password": "longpassword"}

req = requests.post("https://sofomo-assignment.herokuapp.com/login",
     json={"username": "exampleuser", "password": "examplepassword"}).json()

if "access_token" in req:
    auth_token = req["access_token"]
else:
    print(req)

```

url: `/location`

method: `POST`

```python
requests.post("https://sofomo-assignment.herokuapp.com/location",
     json={"address": "www.google.com"},
     headers={"Authorization": f"Bearer {auth_token}"}).json()
```

returns:

- `Address {address} added to the database`

OR

- `Address already in the database`

OR

- `Wrong address`

OR

- `Wrong json`

OR

- `Missing JSON in request.`

method: `DELETE`

```python
requests.delete("https://sofomo-assignment.herokuapp.com/location",
     json={"address": "www.google.com"},
     headers={"Authorization": f"Bearer {auth_token}"}).json()
```

returns:

- `Address {address} deleted from the database`

OR

- `Address not in the database`

OR

- `Wrong address`

OR

- `Wrong json`

OR

- `Missing JSON in request.`

method: `GET`

```python
requests.get("https://sofomo-assignment.herokuapp.com/location",
     json={"address": "www.google.com"},
     headers={"Authorization": f"Bearer {auth_token}"}).json()
```

returns:

Example

- ```json
  {
    "address": "www.olx.pl",
    "ip": "99.84.181.81",
    "type": "ipv4",
    "continent_code": "NA",
    "continent_name": "North America",
    "country_code": "US",
    "country_name": "United States",
    "region_code": "DC",
    "region_name": "Washington",
    "city": "Shaw",
    "zip": "20026",
    "latitude": 38.906898498535156,
    "longitude": -77.02839660644531
  }
  ```

OR

- `Address not in the database`
