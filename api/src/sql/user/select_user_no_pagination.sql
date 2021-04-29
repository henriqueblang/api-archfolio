SELECT
    *
FROM
    archfolio.users
WHERE
    (cast(:username AS TEXT) IS NULL OR username = :username)
