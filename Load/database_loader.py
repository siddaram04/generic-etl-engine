from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from config_loader import load_config
import os
from dotenv import load_dotenv

load_dotenv()

def create_database_connection():

    config = load_config()

    database_config = config["database"]

    username = database_config["username"]
    host = database_config["host"]
    port = database_config["port"]
    database = database_config["database"]

    password = os.getenv("DB_PASSWORD")

    if not password:
        raise ValueError("DB_PASSWORD is not set in the .env file")
    
    connection_url = URL.create(
        drivername="postgresql+psycopg",
        username=username,
        password=password,
        host=host,
        port=port,
        database=database
    )

    engine = create_engine(connection_url)

    return engine


if __name__ == "__main__":

    engine = create_database_connection()

    with engine.connect() as connection:
        print("Successfully connected to PostgreSQL!")