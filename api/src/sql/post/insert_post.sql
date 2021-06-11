INSERT INTO
    archfolio.posts(user_id, title, description, tags, pfp_url)
VALUES
    (
        :author,
        :title,
        :description,
        :tags,
        :pfp_url
    )
RETURNING
    *
