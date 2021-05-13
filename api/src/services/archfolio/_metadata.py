async def create_metadata(self, fields):
    # Receives:
    #   post_id
    #   content
    #   disposition_order
    # Stores picture in Gyazo
    # Inserts into database

    if fields["is_url"]:
        picture = fields["content"]

        fields["content"] = (
            self.get_instance().client.upload_image(picture.file).to_dict()
        )["url"]

    return await self.insert_data("metadata/insert_metadata", fields)


async def get_metadatas(self, fields):
    # Receive:
    #   post_id
    #   offset [None]
    #   fetch [None]
    # Looks in database for:
    #   metadatas with given post_id

    query = "metadata/select_metadata"

    if (
        "offset" not in fields
        or fields["offset"] is None
        or "fetch" not in fields
        or fields["fetch"] is None
    ):
        query = "post/select_metadata_no_pagination"

        fields.pop("offset", None)
        fields.pop("fetch", None)

    return await self.select_data(query, fields)


async def update_metadata(self, fields):
    # Receives:
    #   id
    #   content [None]
    #   disposition_order [None]

    if fields["content"] is None:
        fields["is_url"] = None
    else:
        fields["is_url"] = isinstance(fields["content"], str)

        if fields["is_url"]:
            picture = fields["content"]

            fields["content"] = (
                self.get_instance().client.upload_image(picture.file).to_dict()
            )["url"]

    return await self.update_data("metadata/update_metadata", fields)


async def delete_metadatas(self, fields):
    # Receives:
    #   post_id
    #   id [None]
    # Deletes in database:
    #   metadata with given id from post
    #   or all metadata from post

    if "id" not in fields:
        fields["id"] = None

    return await self.delete_data("metadata/delete_metadata", fields)
