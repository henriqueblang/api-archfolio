INSERT INTO
    archfolio.comments(user_id, post_id, content)
VALUES
    (
        :user_id,
        :post_id,
        :content
    )
RETURNING
    *
