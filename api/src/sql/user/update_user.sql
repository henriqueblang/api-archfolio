UPDATE
    archfolio.users
SET
    username = COALESCE(cast(:username AS TEXT), username),
    salt = COALESCE(cast(:salt AS BYTEA), salt),
    password = COALESCE(cast(:password AS BYTEA), password),
    pfp_url = COALESCE(cast(:pfp_url AS TEXT), pfp_url),
    name = COALESCE(cast(:name AS TEXT), name),
    description = COALESCE(cast(:description AS TEXT), description),
    location = COALESCE(cast(:location AS TEXT), location)
WHERE
    id = :id
RETURNING
    *
