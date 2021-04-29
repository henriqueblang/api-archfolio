SELECT
    id,
    pfp_url,
    description,
    location,
    joined_at
FROM
    archfolio.users
WHERE
    username = :username
    AND
    password = :salted_password
