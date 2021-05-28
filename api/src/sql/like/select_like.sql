SELECT
    *
FROM
    archfolio.likes
WHERE
    post_id = :post_id
    AND
    (cast(:user_id AS INT) IS NULL OR user_id = :user_id)
ORDER BY (SELECT NULL) OFFSET :offset ROWS FETCH NEXT :fetch ROWS ONLY
