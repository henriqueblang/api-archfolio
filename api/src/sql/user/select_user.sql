SELECT
    *
FROM
    archfolio.users
WHERE
    (cast(:username AS TEXT) IS NULL OR username = :username)
ORDER BY (SELECT NULL) OFFSET :offset ROWS FETCH NEXT :fetch ROWS ONLY