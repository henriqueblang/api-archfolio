from fastapi import APIRouter
from src.utils import routing

from .endpoints import user

hierarchical_routers = [
    [
        # Topmost level
        (user.router, "/users", []),
    ],
]

api_router = routing.build_hierarchical_routing(hierarchical_routers)
