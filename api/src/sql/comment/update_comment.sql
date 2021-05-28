UPDATE
    archfolio.comments
SET
    content = COALESCE(cast(:content AS TEXT), content)
WHERE
    id = :id
RETURNING
    *
