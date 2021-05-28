INSERT INTO
    archfolio.favorites(user_id, post_id)
VALUES
    (
        :user_id,
        :post_id
    )
RETURNING
    *
