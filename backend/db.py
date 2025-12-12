import os
from databases import Database
from dotenv import load_dotenv

env = os.getenv("APP_ENV", "local")

if env == "docker":
    load_dotenv(".env.docker")
else:
    load_dotenv(".env.local")

user = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]
db_name = os.environ["POSTGRES_DB"]
host = os.environ["POSTGRES_HOST"]

DATABASE_URL = f"postgresql://{user}:{password}@{host}:5432/{db_name}"
database = Database(DATABASE_URL)