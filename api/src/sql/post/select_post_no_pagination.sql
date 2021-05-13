SELECT
    *
FROM
    archfolio.posts
WHERE
    (cast(:author AS INT) IS NULL OR user_id = :author)
    AND
    (cast(:tags AS TEXT[]) IS NULL OR tags @> :tags)
    AND
    (cast(:title AS TEXT) IS NULL OR title LIKE '%' || :title || '%')
    AND
    (
        cast(:username AS TEXT) IS NULL
        OR
        user_id IN (
            SELECT
                id
            FROM
                archfolio.users
            WHERE
                username LIKE '%' || :username || '%'
        )
    )
    AND
    (
        cast(:name AS TEXT) IS NULL
        OR
        user_id IN (
            SELECT
                id
            FROM
                archfolio.users
            WHERE
                name LIKE '%' || :name || '%'
        )
    )
    AND
    (cast(:start_date AS TIMESTAMP) IS NULL OR created_at >= :start_date)
    AND
    (cast(:end_date AS TIMESTAMP) IS NULL OR created_at <= :end_date)
