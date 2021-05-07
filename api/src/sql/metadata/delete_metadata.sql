DELETE FROM
    archfolio.metadatas
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
