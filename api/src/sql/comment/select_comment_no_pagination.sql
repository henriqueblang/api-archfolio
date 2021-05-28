SELECT
    *
FROM
    archfolio.comments
WHERE
    post_id = :post_id
    AND
    (cast(:user_id AS INT) IS NULL OR user_id = :user_id)
    AND
    (cast(:start_date AS TIMESTAMP) IS NULL OR created_at >= :start_date)
    AND
    (cast(:end_date AS TIMESTAMP) IS NULL OR created_at <= :end_date)
