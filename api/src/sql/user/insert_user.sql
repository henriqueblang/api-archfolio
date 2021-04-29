INSERT INTO
    archfolio.users(username, salt, password, pfp_url, description, location)
VALUES
    (
        :username,
        :salt,
        :password,
        :pfp_url,
        :description,
        :location
    )
RETURNING
    *
