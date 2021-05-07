SELECT
    *
FROM
    archfolio.users as users
INNER JOIN
    archfolio.followers as followers
ON
    users.id = followers.follower_id
WHERE
    followers.following_id = :id
ORDER BY (SELECT NULL) OFFSET :offset ROWS FETCH NEXT :fetch ROWS ONLY
