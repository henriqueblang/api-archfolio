UPDATE
    archfolio.metadatas
SET
    is_url = COALESCE(cast(:is_url AS BOOLEAN), is_url),
    content = COALESCE(cast(:content AS TEXT), content),
    disposition_order = COALESCE(cast(:disposition_order AS INT), disposition_order),
WHERE
    id = :id
RETURNING
    *
