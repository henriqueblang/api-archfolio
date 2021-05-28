DELETE FROM
    archfolio.comments
WHERE
    post_id = :post_id
    AND
    (
        cast(:id AS INT) IS NULL
        OR
        id = :id
    )
RETURNING
    *
