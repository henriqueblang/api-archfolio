INSERT INTO
    archfolio.posts(user_id, title, description, tags)
VALUES
    (
        :author,
        :title,
        :description,
        :tags
    )
RETURNING
    *
