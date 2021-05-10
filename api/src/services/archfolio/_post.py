async def create_post(self, fields):
    # Receives
    #   author
    #   title
    #   description
    #   tags
    # Inserts into database

    return await self.insert_data("post/insert_post", fields)


async def get_posts(self, fields):
    # Receives:
    #   author [None]
    #   tags [None]
    #   title [None]
    #   username [None]
    #   name [None]
    #   start_date [None]
    #   end_date [None]
    #   offset [None]
    #   fetch [None]
    # Looks in database for:
    #   posts with given author
    #   or posts containing the given tags
    #   or posts containing the given title, username, or name

    if "author" not in fields:
        fields["author"] = None

    if "tags" not in fields:
        fields["tags"] = None

    if "title" not in fields:
        fields["title"] = None

    if "username" not in fields:
        fields["username"] = None

    if "name" not in fields:
        fields["name"] = None

    if "start_date" not in fields:
        fields["start_date"] = None

    if "end_date" not in fields:
        fields["end_date"] = None

    query = "post/select_post"

    if (
        "offset" not in fields
        or fields["offset"] is None
        or "fetch" not in fields
        or fields["fetch"] is None
    ):
        query = "post/select_post_no_pagination"

        fields.pop("offset", None)
        fields.pop("fetch", None)

    return await self.select_data(query, fields)


async def update_post(self, fields):
    # Receives:
    #   id
    #   title [None]
    #   description [None]
    #   tags [None]
    #   views [None]

    if "title" not in fields:
        fields["title"] = None

    if "description" not in fields:
        fields["description"] = None

    if "tags" not in fields:
        fields["tags"] = None

    if "views" not in fields:
        fields["views"] = None

    return await self.update_data("post/update_post", fields)


async def delete_posts(self, fields):
    # Receives:
    #   id [None]
    # Deletes in database:
    #   post with given id
    #   or all posts

    if "id" not in fields:
        fields["id"] = None

    return await self.delete_data("post/delete_post", fields)
