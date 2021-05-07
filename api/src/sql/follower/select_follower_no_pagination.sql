SELECT
    *
FROM
    archfolio.users as users
INNER JOIN
    archfolio.followers as followers
ON
    users.id = followers.following_id
WHERE
    followers.follower_id = :id
