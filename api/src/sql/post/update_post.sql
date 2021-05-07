UPDATE
    archfolio.posts
SET
    title = COALESCE(cast(:title AS TEXT), title),
    description = COALESCE(cast(:description AS TEXT), description),
    tags = COALESCE(cast(:tags AS TEXT[]), tags),
    views = COALESCE(cast(:views AS INT), views)
WHERE
    id = :id
RETURNING
    *
