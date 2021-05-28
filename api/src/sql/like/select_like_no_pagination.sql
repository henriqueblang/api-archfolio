SELECT
    *
FROM
    archfolio.likes
WHERE
    post_id = :post_id
    AND
    (cast(:user_id AS INT) IS NULL OR user_id = :user_id)
