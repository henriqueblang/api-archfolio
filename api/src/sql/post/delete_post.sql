DELETE FROM
    archfolio.posts
WHERE
    cast(:id AS INT) IS NULL
    OR
    id = :id
RETURNING
    *
