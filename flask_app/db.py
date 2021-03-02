import os
import psycopg2

DATABASE_HOST = os.environ["DATABASE_HOST"]
DATABASE_USER = os.environ["DATABASE_USER"]
DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]
DATABASE_DATABASE = os.environ["DATABASE_DATABASE"]


conn = psycopg2.connect(
    host=DATABASE_HOST,
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
    database=DATABASE_DATABASE,
)
