from typing import List, Tuple

from fastapi import APIRouter


def build_hierarchical_routing(hierarchical_routers: List[List[Tuple]]) -> APIRouter:
    """

    Instantiates, builds and appends API Routers in a hierarchical distribution.
    Lower level routers path is prefixed with higher level routers path.

    Receives:
        * List of List of Tuples, with APIRouter object, path to be
        appended, and upper-level paths connected to it.
    Returns:
        * APIRouter at the topmost level.

    Ex.:

    [
        [
            (APIRouter(), "/{lower_id}/d", [0])
        ],
        [
            (APIRouter(), "/{upper_id}/b", [0]),
            (APIRouter(), "/{upper_id}/c", [0])
        ],
        [
            (APIRouter(), "/a", [])
        ]
    ]

    will result in the following paths:

    > /a
    > /a/upper_id/b
    > /a/upper_id/c
    > /a/upper_id/b/lower_id/d

    """

    api_router = APIRouter()

    hierarchical_level = len(hierarchical_routers)
    for i, specifications in enumerate(hierarchical_routers):
        routers = [APIRouter() for i in range(len(specifications))]

        for j, router in enumerate(routers):
            local_level_router, local_level_path, upper_level_paths = specifications[j]

            router.include_router(local_level_router, prefix=local_level_path)

            if i == hierarchical_level - 1:
                api_router.include_router(router)
            else:
                next_hierarchical_routers = hierarchical_routers[i + 1]

                for k, next_specifications in enumerate(next_hierarchical_routers):
                    if k not in upper_level_paths:
                        continue

                    next_router = next_specifications[0]

                    next_router.include_router(router)

    return api_router
