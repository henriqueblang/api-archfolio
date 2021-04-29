INSERT INTO
    archfolio.users(username, salt, password, name, description, location)
VALUES
    (
        :username,
        :salt,
        :password,
        :name,
        :description,
        :location
    )
RETURNING
    *
