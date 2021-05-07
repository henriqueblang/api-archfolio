INSERT INTO
    archfolio.users(username, email, salt, password, pfp_url, name, description, location)
VALUES
    (
        :username,
        :email,
        :salt,
        :password,
        :pfp_url,
        :name,
        :description,
        :location
    )
RETURNING
    *
