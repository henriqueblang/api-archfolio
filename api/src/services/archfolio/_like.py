async def like_post(self, fields):
    # Receives:
    #   post_id
    #   user_id
    # Inserts into database

    return await self.insert_data("like/insert_like", fields)


async def get_likes(self, fields):
    # Receives:
    #   post_id
    #   user_id [None]
    #   offset [None]
    #   fetch [None]
    #   Looks in database for:
    #       all likes from post
    #       or like in post from user

    if "user_id" not in fields:
        fields["user_id"] = None

    query = "like/select_like"

    if (
        "offset" not in fields
        or fields["offset"] is None
        or "fetch" not in fields
        or fields["fetch"] is None
    ):
        query = "like/select_like_no_pagination"

        fields.pop("offset", None)
        fields.pop("fetch", None)

    return await self.select_data(query, fields)


async def delete_likes(self, fields):
    # Receives:
    #   post_id
    #   user_id [None]
    # Deletes in database:
    #   likes from post
    #   or like in post from user

    if "user_id" not in fields:
        fields["user_id"] = None

    return await self.delete_data("like/delete_like", fields)
