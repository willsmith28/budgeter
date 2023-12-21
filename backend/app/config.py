"""Configuration values"""
import os

SECRET_KEY = os.environ["SECRET_KEY"]
SQL_HOST = os.environ["SQL_HOST"]
SQL_PORT = os.environ["SQL_PORT"]
POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_DB = os.environ["POSTGRES_DB"]

POSTGRES_CONNINFO = f"""
    dbname={POSTGRES_DB}
    user={POSTGRES_USER}
    password={POSTGRES_PASSWORD}
    host={SQL_HOST}
    port={SQL_PORT}
"""
