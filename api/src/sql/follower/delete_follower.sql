DELETE FROM
    archfolio.followers
WHERE
    follower_id = :id
    AND
    (
        cast(:following_id AS INT) IS NULL
        OR
        following_id = :following_id
    )
RETURNING
    *
