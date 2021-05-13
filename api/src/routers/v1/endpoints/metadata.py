from typing import Optional

from asyncpg.exceptions import (
    InvalidRowCountInLimitClauseError,
    InvalidRowCountInResultOffsetClauseError,
    NotNullViolationError,
    StringDataRightTruncationError,
)
from fastapi import APIRouter, File, Form, Header, UploadFile
from pydantic import Json
from src.schemas.metadata import Metadata, UpdateMetadata
from src.services.archfolio import Archfolio
from src.utils import errors

router = APIRouter()


@router.post("")
async def create_metadata(
    post_id: int,
    text: Json[Metadata] = Form(...),
    file: Optional[UploadFile] = File(None),
):
    metadata_dict = text.dict()

    metadata_dict["post_id"] = post_id
    metadata_dict["is_url"] = False

    if file is not None:
        metadata_dict["is_url"] = True
        metadata_dict["content"] = file

    try:
        result = await Archfolio.get_instance().create_metadata(metadata_dict)
    except NotNullViolationError:
        errors.raise_error_response(errors.ErrorResourceNotFound)
    except Exception:
        errors.raise_error_response(errors.ErrorInternal)

    return result


@router.get("")
async def get_metadatas(
    post_id: int,
    offset: Optional[int] = None,
    fetch: Optional[int] = None,
):
    fields = {
        "post_id": post_id,
        "offset": offset,
        "fetch": fetch,
    }

    try:
        result = await Archfolio.get_instance().get_metadatas(fields)
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


@router.get("/{id}")
async def update_metadata(
    id: int,
    text: Json[UpdateMetadata] = Form(...),
    file: Optional[UploadFile] = File(None),
):
    metadata_dict = update_metadata.dict()

    metadata_dict["id"] = id

    if file is not None:
        metadata_dict["content"] = file

    try:
        result = await Archfolio.get_instance().update_metadata(metadata_dict)
    except StringDataRightTruncationError:
        errors.raise_error_response(errors.ErrorResourceDataInvalid)
    except Exception:
        errors.raise_error_response(errors.ErrorInternal)

    if result is None:
        errors.raise_error_response(errors.ErrorResourceNotFound)

    return result


@router.delete("/{id}")
async def delete_metadatas(
    post_id: int,
    id: int,
):
    fields = {
        "post_id": post_id,
        "id": id,
    }

    try:
        result = await Archfolio.get_instance().delete_metadatas(fields)
    except Exception:
        errors.raise_error_response(errors.ErrorInternal)

    if result is None:
        errors.raise_error_response(errors.ErrorResourceNotFound)

    return result
