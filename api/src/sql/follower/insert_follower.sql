INSERT INTO
    archfolio.followers(follower_id, following_id)
VALUES
    (
        :id,
        (
            SELECT
                id
            FROM
                archfolio.users
            WHERE
                username = :identification
                OR
                email = :identification
        )
    )
RETURNING
    *
