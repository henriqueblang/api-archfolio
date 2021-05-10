from typing import Optional

from asyncpg.exceptions import (
    InvalidRowCountInLimitClauseError,
    InvalidRowCountInResultOffsetClauseError,
    NotNullViolationError,
)
from fastapi import APIRouter
from src.schemas.follower import Follower
from src.services.archfolio import Archfolio
from src.utils import errors

router = APIRouter()


@router.post("")
async def follow_user(
    id: int,
    follower: Follower,
):
    follower_dict = follower.dict()

    follower_dict["id"] = id

    try:
        result = await Archfolio.get_instance().follow_user(follower_dict)
    except NotNullViolationError:
        errors.raise_error_response(errors.ErrorResourceNotFound)
    except Exception:
        errors.raise_error_response(errors.ErrorInternal)

    return result


@router.get("")
async def get_followers(
    id: int,
    offset: Optional[int] = None,
    fetch: Optional[int] = None,
):
    fields = {
        "id": id,
        "offset": offset,
        "fetch": fetch,
    }

    try:
        result = await Archfolio.get_instance().get_followers(fields)
    except (
        InvalidRowCountInResultOffsetClauseError,
        InvalidRowCountInLimitClauseError,
    ):
        errors.raise_error_response(errors.ErrorResourceDataInvalid)
    except Exception:
        errors.raise_error_response(errors.ErrorInternal)

    if not result:
        errors.raise_error_response(errors.ErrorResourceNotFound)

    return result


@router.delete("/{following_id}")
async def delete_follower(
    id: int,
    following_id: int,
):
    fields = {
        "id": id,
        "following_id": following_id,
    }

    try:
        result = await Archfolio.get_instance().delete_follower(fields)
    except Exception:
        errors.raise_error_response(errors.ErrorInternal)

    if result is None:
        errors.raise_error_response(errors.ErrorResourceNotFound)

    return result
