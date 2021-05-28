async def favorite_post(self, fields):
    # Receives:
    #   post_id
    #   user_id
    # Inserts into database

    return await self.insert_data("favorite/insert_favorite", fields)


async def get_favorites(self, fields):
    # Receives:
    #   post_id
    #   user_id [None]
    #   start_date [None]
    #   end_date [None]
    #   offset [None]
    #   fetch [None]
    #   Looks in database for:
    #       all favorites from post
    #       or favorite in post from user

    if "user_id" not in fields:
        fields["user_id"] = None

    query = "favorite/select_favorite"

    if (
        "offset" not in fields
        or fields["offset"] is None
        or "fetch" not in fields
        or fields["fetch"] is None
    ):
        query = "favorite/select_favorite_no_pagination"

        fields.pop("offset", None)
        fields.pop("fetch", None)

    return await self.select_data(query, fields)


async def delete_favorites(self, fields):
    # Receives:
    #   post_id
    #   user_id [None]
    # Deletes in database:
    #   favorites from post
    #   or favorite in post from user

    if "user_id" not in fields:
        fields["user_id"] = None

    return await self.delete_data("favorite/delete_favorite", fields)
