import hashlib
import hmac
import os
from typing import Tuple


def __hash_new_password(password: str) -> Tuple[bytes, bytes]:
    """
    Hash the provided password with a randomly-generated salt and return the
    salt and hash to store in the database.
    """
    salt = os.urandom(16)
    pw_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return salt, pw_hash


def __is_correct_password(salt: bytes, pw_hash: bytes, password: str) -> bool:
    """
    Given a previously-stored salt and hash, and a password provided by a user
    trying to log in, check whether the password is correct.
    """
    return hmac.compare_digest(
        pw_hash, hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    )


async def create_user(self, fields):
    # Receives:
    #   username
    #   password
    #   profile_picture
    #   name
    #   description
    #   location
    # Generates salt and hashes password
    # Inserts into database
    # Stores profile picture in Gyazo
    # Updates profile picture URL in database

    user = None

    async with self.get_instance().session.transaction():
        salt, pw_hash = __hash_new_password(fields["password"])

        fields["salt"] = salt
        fields["password"] = pw_hash

        user = await self.insert_data("user/insert_user", fields)

        profile_picture = fields["profile_picture"]
        if profile_picture is not None:
            image = self.get_instance().client.upload_image(profile_picture)

            upload_information = image.to_dict()

            fields.clear()
            fields["id"] = user["id"]
            fields["pfp_url"] = upload_information["url"]

            user = await self.update_user(fields)

    return user


async def get_user(self, fields):
    # Receives:
    #   username
    #   password
    # Looks in database for:
    #   user matching username
    # Compares given password with stored salted and hashed password

    user = await self.select_data("user/select_user_no_pagination", fields, all=False)

    if not user:
        return None

    salt = user["salt"]
    pw_hash = user["password"]

    if not __is_correct_password(salt, pw_hash, fields["password"]):
        return False

    return user


async def update_user(self, fields):
    # Receives
    #   id
    #   username [None]
    #   salt [None]
    #   password [None]
    #   profile_picture [None]
    #   name [None]
    #   description [None]
    #   location [None]
    # Stores profile picture in Gyazo
    # Updates in database

    if "username" not in fields:
        fields["username"] = None

    if "salt" not in fields:
        fields["salt"] = None

    if "password" not in fields:
        fields["password"] = None

    if "profile_picture" not in fields:
        fields["profile_picture"] = None

    if "name" not in fields:
        fields["name"] = None

    if "description" not in fields:
        fields["description"] = None

    if "location" not in fields:
        fields["location"] = None

    profile_picture = fields["profile_picture"]
    if profile_picture is not None:
        image = self.get_instance().client.upload_image(profile_picture)

        upload_information = image.to_dict()

        fields["pfp_url"] = upload_information["url"]

    return await self.update_data("user/update_user", fields)


async def delete_users(self, fields):
    # Receives
    #   id [None]
    # Deletes in database:
    #   user with given id
    #   or all users

    if "id" not in fields:
        fields["id"] = None

    return await self.delete_data("user/delete_user", fields)
