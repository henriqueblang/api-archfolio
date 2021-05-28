from typing import Optional

from asyncpg.exceptions import (
    InvalidRowCountInLimitClauseError,
    InvalidRowCountInResultOffsetClauseError,
    NotNullViolationError,
)
from fastapi import APIRouter
from src.schemas.favorite import Favorite
from src.services.archfolio import Archfolio
from src.utils import errors

router = APIRouter()


@router.post("")
async def favorite_post(
    post_id: int,
    favorite: Favorite,
):
    favorite_dict = favorite.dict()

    favorite_dict["post_id"] = post_id

    try:
        result = await Archfolio.get_instance().favorite_post(favorite_dict)
    except NotNullViolationError:
        errors.raise_error_response(errors.ErrorResourceNotFound)
    except Exception:
        errors.raise_error_response(errors.ErrorInternal)

    return result


@router.get("")
async def get_favorites(
    post_id: int,
    user_id: Optional[int] = None,
    offset: Optional[int] = None,
    fetch: Optional[int] = None,
):
    fields = {
        "post_id": post_id,
        "user_id": user_id,
        "offset": offset,
        "fetch": fetch,
    }

    try:
        result = await Archfolio.get_instance().get_favorites(fields)
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


@router.delete("/{user_id}")
async def delete_follower(
    post_id: int,
    user_id: int,
):
    fields = {
        "post_id": post_id,
        "user_id": user_id,
    }

    try:
        result = await Archfolio.get_instance().delete_favorites(fields)
    except Exception:
        errors.raise_error_response(errors.ErrorInternal)

    if result is None:
        errors.raise_error_response(errors.ErrorResourceNotFound)

    return result
