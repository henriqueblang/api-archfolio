SELECT
    *
FROM
    archfolio.posts
WHERE
    (cast(:author AS INT) IS NULL OR user_id = :author)
    OR
    (cast(:tags AS TEXT[]) IS NULL OR tags @> :tags)
    OR
    (cast(:title AS TEXT) IS NULL OR title LIKE '%' || :title || '%')
    OR
    (
        cast(:username AS TEXT) IS NULL
        OR
        user_id = (
            SELECT
                id
            FROM
                archfolio.users
            WHERE
                username LIKE '%' || :username || '%'
        )
    )
    OR
    (
        cast(:name AS TEXT) IS NULL
        OR
        user_id = (
            SELECT
                id
            FROM
                archfolio.users
            WHERE
                name LIKE '%' || :name || '%'
        )
    )
ORDER BY (SELECT NULL) OFFSET :offset ROWS FETCH NEXT :fetch ROWS ONLY
