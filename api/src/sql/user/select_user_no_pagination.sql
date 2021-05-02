SELECT
    *
FROM
    archfolio.users
WHERE
    (cast(:identification AS TEXT) IS NULL OR username = :identification)
    OR
    (cast(:identification AS TEXT) IS NULL OR email = :identification)
