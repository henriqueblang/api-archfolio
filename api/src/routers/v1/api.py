from fastapi import APIRouter
from src.utils import routing

hierarchical_routers = []

api_router = routing.build_hierarchical_routing(hierarchical_routers)
