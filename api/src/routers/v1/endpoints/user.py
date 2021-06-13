from typing import Optional

from asyncpg.exceptions import StringDataRightTruncationError, UniqueViolationError
from fastapi import APIRouter, File, Form, UploadFile
from pydantic import Json
from src.schemas.user import UpdateUser, User
from src.services.archfolio import Archfolio
from src.utils import errors

router = APIRouter()


@router.post("")
async def create_user(
    text: Json[User] = Form(...),
    file: Optional[UploadFile] = File(None),
):
    user_dict = text.dict()

    user_dict["profile_picture"] = file

    try:
        result = await Archfolio.get_instance().create_user(user_dict)
    except StringDataRightTruncationError:
        errors.raise_error_response(errors.ErrorResourceDataInvalid)
    except UniqueViolationError:
        errors.raise_error_response(errors.ErrorDuplicateResource)
    except Exception:
        errors.raise_error_response(errors.ErrorInternal)

    if result is None:
        errors.raise_error_response(errors.ErrorInternal)

    result = {k: v for k, v in result.items() if not isinstance(v, bytes)}

    return result


@router.get("")
async def get_users(
    id: Optional[int] = None,
    identification: Optional[str] = None,
    password: Optional[str] = None,
):
    fields = {"id": id, "identification": identification, "password": password}

    try:
        result = await Archfolio.get_instance().get_users(fields)
    except Exception:
        errors.raise_error_response(errors.ErrorInternal)

    if result is None:
        errors.raise_error_response(errors.ErrorResourceNotFound)
    elif not result:
        errors.raise_error_response(errors.ErrorAuthorizationForbidden)

    return result


@router.patch("/{id}")
async def update_user(
    id: int,
    text: Json[UpdateUser] = Form(...),
    file: Optional[UploadFile] = File(None),
):
    user_dict = text.dict()

    user_dict["id"] = id
    user_dict["profile_picture"] = file

    try:
        result = await Archfolio.get_instance().update_user(user_dict)
    except StringDataRightTruncationError:
        errors.raise_error_response(errors.ErrorResourceDataInvalid)
    except UniqueViolationError:
        errors.raise_error_response(errors.ErrorDuplicateResource)
    except Exception:
        errors.raise_error_response(errors.ErrorInternal)

    if result is None:
        errors.raise_error_response(errors.ErrorResourceNotFound)

    result = {k: v for k, v in result.items() if not isinstance(v, bytes)}

    return result


@router.delete("/{id}")
async def delete_user(id: int):
    fields = {
        "id": id,
    }

    try:
        result = await Archfolio.get_instance().delete_users(fields)
    except Exception:
        errors.raise_error_response(errors.ErrorInternal)

    if result is None:
        errors.raise_error_response(errors.ErrorResourceNotFound)

    result = {k: v for k, v in result.items() if not isinstance(v, bytes)}

    return result
