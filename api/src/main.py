import importlib
import logging

from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.config import settings
from src.services.archfolio import Archfolio
from src.utils import errors
from starlette.exceptions import HTTPException as StarletteHTTPException

# Import module corresponding to API version in settings
api_version = settings.settings.API_URL.split("/")[-1]
api_module = importlib.import_module(f"src.routers.{api_version}.api")

instance = Archfolio.get_instance()

app = FastAPI(
    title="API Archfolio",
    version="1.0.0",
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_data = dict(errors.ErrorResourceInvalid.error)
    error_data["detail"] = exc.errors()

    return JSONResponse(
        status_code=errors.ErrorResourceInvalid.status_code,
        content=jsonable_encoder({"error": error_data}),
    )


@app.exception_handler(StarletteHTTPException)
async def unicorn_exception_handler(request: Request, exc: StarletteHTTPException):
    error_status_code, error_detail = exc.status_code, exc.detail

    if isinstance(error_detail, str):
        if error_status_code == errors.ErrorRouteNotFound.status_code:
            error_detail = errors.ErrorRouteNotFound.error
        elif error_status_code == errors.ErrorMethodNotAllowed.status_code:
            error_detail = errors.ErrorMethodNotAllowed.error

    return JSONResponse(
        status_code=error_status_code,
        content={"error": error_detail},
    )


@app.on_event("startup")
async def startup():
    try:
        await instance.open()
    except Exception as e:
        logging.critical("Could not connect to database: " + str(e))


@app.on_event("shutdown")
async def shutdown():
    await instance.close()


app.include_router(api_module.api_router, prefix=settings.settings.API_URL)
