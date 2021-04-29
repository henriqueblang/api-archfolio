from gyazo import Api
from src.config import settings
from src.repository.database import Database


# https://stackoverflow.com/questions/47561840/python-how-can-i-separate-functions-of-class-into-multiple-files
class Archfolio(Database):
    client = Api(access_token=settings.settings.KEYS["GYAZO"])

    from ._user import create_user, delete_users, get_user, update_user
