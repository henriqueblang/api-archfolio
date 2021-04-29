import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """ Configurações globais """

    API_URL: str = "/archfolio/v1"

    DATABASE = {
        "host": os.getenv("POSTGRE_HOST"),
        "user": os.getenv("POSTGRE_USER"),
        "port": os.getenv("POSTGRE_PORT"),
        "password": os.getenv("POSTGRE_PASSWORD"),
        "database": os.getenv("POSTGRE_DATABASE"),
    }

    KEYS = {
        "GYAZO": os.getenv("GYAZO_KEY"),
    }


settings = Settings()
