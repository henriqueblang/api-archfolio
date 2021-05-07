INSERT INTO
    archfolio.metadatas(post_id, is_url, content, disposition_order)
VALUES
    (
        :post_id,
        :is_url,
        :content,
        :disposition_order
    )
RETURNING
    *
