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
    #   email
    #   password
    #   profile_picture [None]
    #   name
    #   description [None]
    #   location [None]
    # Generates salt and hashes password
    # Stores profile picture in Gyazo
    # Inserts into database

    salt, pw_hash = __hash_new_password(fields["password"])

    fields["salt"] = salt
    fields["password"] = pw_hash

    profile_picture = fields.pop("profile_picture", None)

    fields["pfp_url"] = (
        (self.get_instance().client.upload_image(profile_picture.file).to_dict())["url"]
        if profile_picture is not None
        else None
    )

    return await self.insert_data("user/insert_user", fields)


async def get_users(self, fields):
    # Receives:
    #   id [None]
    #   identification [None]
    #   password [None]
    # Looks in database for:
    #   user matching id or identification (username or email)
    # Compares given password with stored salted and hashed password

    if "id" not in fields:
        fields["id"] = None

    if "identification" not in fields:
        fields["identification"] = None

    user = await self.select_data(
        "user/select_user_no_pagination",
        {
            "id": fields["id"],
            "identification": fields["identification"],
        },
        all=False,
    )

    if not user:
        return None

    if fields["password"] is not None:
        salt = user["salt"]
        pw_hash = user["password"]

        if not __is_correct_password(salt, pw_hash, fields["password"]):
            return False

    return user


async def update_user(self, fields):
    # Receives
    #   id
    #   username [None]
    #   email [None]
    #   password [None]
    #   profile_picture [None]
    #   name [None]
    #   description [None]
    #   location [None]
    # Stores profile picture in Gyazo
    # Updates in database

    if fields["password"] is not None:
        salt, pw_hash = __hash_new_password(fields["password"])

        fields["salt"] = salt
        fields["password"] = pw_hash
    else:
        fields["salt"] = None

    if fields["profile_picture"] is None:
        fields["pfp_url"] = None
    else:
        profile_picture = fields["profile_picture"]

        image = self.get_instance().client.upload_image(profile_picture.file).to_dict()

        fields["pfp_url"] = image["url"]

    return await self.update_data(
        "user/update_user",
        {
            "id": fields["id"],
            "username": fields["username"],
            "email": fields["email"],
            "salt": fields["salt"],
            "password": fields["password"],
            "pfp_url": fields["pfp_url"],
            "name": fields["name"],
            "description": fields["description"],
            "location": fields["location"],
        },
    )


async def delete_users(self, fields):
    # Receives
    #   id [None]
    # Deletes in database:
    #   user with given id
    #   or all users

    if "id" not in fields:
        fields["id"] = None

    return await self.delete_data(
        "user/delete_user",
        {
            "id": fields["id"],
        },
    )
