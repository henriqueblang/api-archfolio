import asyncio
import configparser
import os
from abc import ABC
from urllib.parse import quote_plus as urlquote

import asyncpg
import databases
from src.config import settings


# https://www.encode.io/databases/database_queries/
class Database(ABC):
    session = None
    __instance = None

    def __init__(self):
        self.credentials = self.__get_credentials()

    @classmethod
    def get_instance(self):
        if self.__instance is None:
            self.__instance = self()

        return self.__instance

    def __get_credentials(self):
        return {k: urlquote(v) for k, v in settings.settings.DATABASE.items()}

    def __get_url_postgres(self):
        url_1 = (
            f"postgresql://{self.credentials['user']}:{self.credentials['password']}"
        )
        url_2 = f"{self.credentials['host']}:{self.credentials['port']}/{self.credentials['database']}"

        return f"{url_1}@{url_2}"

    async def open(self):
        if self.session is not None:
            return

        url_database = self.__get_url_postgres()

        self.session = databases.Database(url_database, ssl=True)

        try:
            await self.session.connect()
        except Exception:
            self.session = databases.Database(url_database)

            await self.session.connect()

    async def close(self):
        if self.session is None:
            return

        await self.session.disconnect()

    async def __get_file_query(self, file_name):
        file_path = f"src/sql/{file_name}.sql"

        with open(file_path, "r") as file_query:
            query = file_query.read()

        return query

    async def insert_data(self, file_name, parameters, all=False):
        return await self.__generic_fetch(file_name, parameters, all)

    async def select_data(self, file_name, parameters=None, all=True):
        return await self.__generic_fetch(file_name, parameters, all)

    async def update_data(self, file_name, parameters=None, all=False):
        return await self.__generic_fetch(file_name, parameters, all)

    async def delete_data(self, file_name, parameters=None, all=False):
        return await self.__generic_fetch(file_name, parameters, all)

    async def __generic_fetch(self, file_name, parameters, all):
        query = await self.__get_file_query(file_name)

        # fetch_all returns typing.List[typing.Mapping]
        # fetch_one returns typing.Optional[typing.Mapping]
        command = self.session.fetch_all if all else self.session.fetch_one

        if parameters is None:
            result = await command(query=query)
        else:
            if isinstance(parameters, dict):
                result = await command(query=query, values=parameters)
            else:
                result = []

                for nth_parameters in parameters:
                    result.append(await command(query=query, values=nth_parameters))

        return result
