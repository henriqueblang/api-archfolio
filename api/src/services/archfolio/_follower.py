async def follow_user(self, fields):
    # Receives:
    #   id
    #   identification
    # Inserts into database

    return await self.insert_data("follower/insert_follower", fields)


async def get_followers(self, fields):
    # Receives:
    #   id
    #   offset [None]
    #   fetch [None]
    #   Looks in database for:
    #     users followed by id
    #     and users following id

    follower_query = "follower/select_follower"
    following_query = "follower/select_following"

    if (
        "offset" not in fields
        or fields["offset"] is None
        or "fetch" not in fields
        or fields["fetch"] is None
    ):
        follower_query = "follower/select_follower_no_pagination"
        following_query = "follower/select_following_no_pagination"

        fields.pop("offset", None)
        fields.pop("fetch", None)

    followers_list = await self.select_data(follower_query, fields)
    following_list = await self.select_data(following_query, fields)

    followers_list = [
        {k: v for k, v in follower.items() if not isinstance(v, bytes)}
        for follower in followers_list
    ]

    following_list = [
        {k: v for k, v in following.items() if not isinstance(v, bytes)}
        for following in following_list
    ]

    return {"followers": followers_list, "following": following_list}


async def delete_followers(self, fields):
    # Receives:
    #   id
    #   following_id [None]
    # Deletes in database:
    #   following with given id from user
    #   or all following from user

    if "following_id" not in fields:
        fields["following_id"] = None

    return await self.delete_data("follower/delete_follower", fields)
