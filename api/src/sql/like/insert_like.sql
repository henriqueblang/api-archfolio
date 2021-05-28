INSERT INTO
    archfolio.likes(user_id, post_id)
VALUES
    (
        :user_id,
        :post_id
    )
RETURNING
    *
