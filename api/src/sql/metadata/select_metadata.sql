SELECT
    *
FROM
    archfolio.metadatas
WHERE
    post_id = :post_id
ORDER BY
    disposition_order ASC
OFFSET :offset ROWS FETCH NEXT :fetch ROWS ONLY
