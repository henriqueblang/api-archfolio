from typing import Optional

from asyncpg.exceptions import (
    InvalidRowCountInLimitClauseError,
    InvalidRowCountInResultOffsetClauseError,
    NotNullViolationError,
)
from dateutil import parser
from fastapi import APIRouter
from src.schemas.comment import Comment
from src.services.archfolio import Archfolio
from src.utils import errors

router = APIRouter()


@router.post("")
async def create_comment(
    post_id: int,
    comment: Comment,
):
    comment_dict = comment.dict()

    comment_dict["post_id"] = post_id

    try:
        result = await Archfolio.get_instance().create_comment(comment_dict)
    except NotNullViolationError:
        errors.raise_error_response(errors.ErrorResourceNotFound)
    except Exception:
        errors.raise_error_response(errors.ErrorInternal)

    return result


@router.get("")
async def get_comments(
    post_id: int,
    user_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    offset: Optional[int] = None,
    fetch: Optional[int] = None,
):
    try:
        start_datetime = parser.parse(start_date) if start_date is not None else None
        end_datetime = parser.parse(end_date) if end_date is not None else None
    except Exception:
        errors.raise_error_response(errors.ErrorResourceDataInvalid)

    fields = {
        "post_id": post_id,
        "user_id": user_id,
        "start_date": start_datetime,
        "end_date": end_datetime,
        "offset": offset,
        "fetch": fetch,
    }

    try:
        result = await Archfolio.get_instance().get_comments(fields)
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


@router.delete("/{id}")
async def delete_comment(
    post_id: int,
    id: int,
):
    fields = {
        "post_id": post_id,
        "id": id,
    }

    try:
        result = await Archfolio.get_instance().delete_comments(fields)
    except Exception:
        errors.raise_error_response(errors.ErrorInternal)

    if result is None:
        errors.raise_error_response(errors.ErrorResourceNotFound)

    return result
