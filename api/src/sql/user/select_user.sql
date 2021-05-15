SELECT
    *
FROM
    archfolio.users
WHERE
    (cast(:id AS INT) IS NULL OR id = :id)
    OR
    (cast(:identification AS TEXT) IS NULL OR username = :identification)
    OR
    (cast(:identification AS TEXT) IS NULL OR email = :identification)
ORDER BY (SELECT NULL) OFFSET :offset ROWS FETCH NEXT :fetch ROWS ONLY
