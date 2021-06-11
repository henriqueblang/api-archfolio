from typing import List, Optional

from asyncpg.exceptions import (
    InvalidRowCountInLimitClauseError,
    InvalidRowCountInResultOffsetClauseError,
    StringDataRightTruncationError,
)
from dateutil import parser
from fastapi import APIRouter, File, Form, Query, UploadFile
from pydantic import Json
from src.schemas.post import Post, UpdatePost
from src.services.archfolio import Archfolio
from src.utils import errors

router = APIRouter()


@router.post("")
async def create_post(
    text: Json[Post] = Form(...),
    file: Optional[UploadFile] = File(None),
):
    post_dict = text.dict()

    post_dict["thumbnail"] = file

    try:
        result = await Archfolio.get_instance().create_post(post_dict)
    except StringDataRightTruncationError:
        errors.raise_error_response(errors.ErrorResourceDataInvalid)
    except Exception:
        errors.raise_error_response(errors.ErrorInternal)

    return result


@router.get("")
async def get_posts(
    author: Optional[int] = None,
    tags: Optional[List[str]] = Query(None),
    title: Optional[str] = None,
    username: Optional[str] = None,
    name: Optional[str] = None,
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
        "author": author,
        "tags": tags,
        "title": title,
        "username": username,
        "name": name,
        "start_date": start_datetime,
        "end_date": end_datetime,
        "offset": offset,
        "fetch": fetch,
    }

    try:
        result = await Archfolio.get_instance().get_posts(fields)
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


@router.patch("/{id}")
async def update_post(
    id: int,
    text: Json[UpdatePost] = Form(...),
    file: Optional[UploadFile] = File(None),
):
    post_dict = text.dict()

    post_dict["id"] = id
    post_dict["thumbnail"] = file

    try:
        result = await Archfolio.get_instance().update_post(post_dict)
    except StringDataRightTruncationError:
        errors.raise_error_response(errors.ErrorResourceDataInvalid)
    except Exception:
        errors.raise_error_response(errors.ErrorInternal)

    if result is None:
        errors.raise_error_response(errors.ErrorResourceNotFound)

    return result


@router.delete("/{id}")
async def delete_post(
    id: int,
):
    fields = {
        "id": id,
    }

    try:
        result = await Archfolio.get_instance().delete_posts(fields)
    except Exception:
        errors.raise_error_response(errors.ErrorInternal)

    if result is None:
        errors.raise_error_response(errors.ErrorResourceNotFound)

    return result
