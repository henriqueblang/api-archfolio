INSERT INTO
    archfolio.users(username, email, salt, password, name, description, location)
VALUES
    (
        :username,
        :email,
        :salt,
        :password,
        :name,
        :description,
        :location
    )
RETURNING
    *
