from gyazo import Api
from src.config import settings
from src.repository.database import Database


# https://stackoverflow.com/questions/47561840/python-how-can-i-separate-functions-of-class-into-multiple-files
class Archfolio(Database):
    client = Api(access_token=settings.settings.KEYS["GYAZO"])

    from ._follower import delete_followers, follow_user, get_followers
    from ._metadata import (
        create_metadata,
        delete_metadatas,
        get_metadatas,
        update_metadata,
    )
    from ._post import create_post, delete_posts, get_posts, update_post
    from ._user import create_user, delete_users, get_users, update_user
