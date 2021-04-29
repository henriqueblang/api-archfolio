INSERT INTO
    archfolio.users(username, salt, password, pfp_url, name, description, location)
VALUES
    (
        :username,
        :salt,
        :password,
        :pfp_url,
        :name,
        :description,
        :location
    )
RETURNING
    *
