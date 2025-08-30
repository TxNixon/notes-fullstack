import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from datetime import timedelta

load_dotenv()

def mysql_uri() -> str:
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("DB_NAME", "notes")
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"

class Config:
    SQLALCHEMY_DATABASE_URI = mysql_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET", "123")

    # expires token jwt
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)


def db_connection():
    uri = Config.SQLALCHEMY_DATABASE_URI
    try:
        engine = create_engine(uri)
        connection = engine.connect()
        print("Database connection successful")
        connection.close()
        return True
    except OperationalError as e:
        print(f"Database connection failed: {e}")
        raise RuntimeError(f"Failed to connect to the database: {e}")