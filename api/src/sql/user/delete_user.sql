DELETE FROM
    archfolio.users
WHERE
    cast(:id AS INT) IS NULL
    OR
    id = :id
RETURNING
    *
