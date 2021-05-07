SELECT
    *
FROM
    archfolio.metadatas
WHERE
    post_id = :post_id
ORDER BY (SELECT NULL) OFFSET :offset ROWS FETCH NEXT :fetch ROWS ONLY
