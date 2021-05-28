async def create_comment(self, fields):
    # Receives:
    #   post_id
    #   user_id
    #   content
    # Inserts into database

    return await self.insert_data("comment/insert_comment", fields)


async def get_comments(self, fields):
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

    if "start_date" not in fields:
        fields["start_date"] = None

    if "end_date" not in fields:
        fields["end_date"] = None

    query = "comment/select_comment"

    if (
        "offset" not in fields
        or fields["offset"] is None
        or "fetch" not in fields
        or fields["fetch"] is None
    ):
        query = "comment/select_comment_no_pagination"

        fields.pop("offset", None)
        fields.pop("fetch", None)

    return await self.select_data(query, fields)


async def delete_comments(self, fields):
    # Receives:
    #   post_id
    #   id [None]
    # Deletes in database:
    #   comments from post
    #   or comment in post

    if "id" not in fields:
        fields["id"] = None

    return await self.delete_data("comment/delete_comment", fields)
