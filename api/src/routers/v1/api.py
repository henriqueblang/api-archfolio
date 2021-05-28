from fastapi import APIRouter
from src.utils import routing

from .endpoints import comment, favorite, follower, like, metadata, post, user

hierarchical_routers = [
    # 0
    [
        # Connects into hierarchical_routers[1][0] (/users)
        (follower.router, "/{user_id}/followers", [0]),
        # Connects into hierarchical_routers[1][1] (/posts)
        (metadata.router, "/{post_id}/metadatas", [1]),
        # Connects into hierarchical_routers[1][1] (/posts)
        (comment.router, "/{post_id}/comments", [1]),
        # Connects into hierarchical_routers[1][1] (/posts)
        (favorite.router, "/{post_id}/favorites", [1]),
        # Connects into hierarchical_routers[1][1] (/posts)
        (like.router, "/{post_id}/likes", [1]),
    ],
    # 1
    [
        # Topmost level
        (user.router, "/users", []),
        (post.router, "/posts", []),
    ],
]

api_router = routing.build_hierarchical_routing(hierarchical_routers)
