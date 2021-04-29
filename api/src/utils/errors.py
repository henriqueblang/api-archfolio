from fastapi import HTTPException


def raise_error_response(error, detail=None):
    error_body = dict(error.error)

    if detail is not None:
        error_body["detail"] = detail

    raise HTTPException(
        status_code=error.status_code,
        detail=error_body,
    )


class ErrorResourceInvalid:
    status_code = 400

    error = {
        "type": "invalid_resource",
        "description": "The requested resource is invalid.",
    }


class ErrorResourceDataInvalid:
    status_code = 400

    error = {
        "type": "invalid_resource_data",
        "description": "The requested resource contains invalid data.",
    }


class ErrorRouteNotFound:
    status_code = 404

    error = {
        "type": "route_not_found",
        "description": "The requested route does not exist.",
    }


class ErrorResourceNotFound:
    status_code = 404

    error = {
        "type": "resource_not_found",
        "description": "The requested resource does not exist.",
    }


class ErrorMethodNotAllowed:
    status_code = 405

    error = {
        "type": "method_not_allowed",
        "description": "The requested resource does not allow this action.",
    }


class ErrorDuplicateResource:
    status_code = 409

    error = {
        "type": "duplicate_resource",
        "description": "The requested resource is already registered.",
    }


class ErrorInternal:
    status_code = 500

    error = {
        "type": "internal_error",
        "description": "An internal error has occurred while processing the request.",
    }
