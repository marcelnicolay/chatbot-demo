import os
import logging

from fastapi import FastAPI, FastAPI, Request, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from src.api.threads.router import router as ThreadRouter
from src.api.threads.models import ThreadInDb
from src.errors import NoResultFound
from .db.mongodb_utils import close_mongo_connection, connect_to_mongo


app = FastAPI()
app.include_router(ThreadRouter, prefix="/api/threads")

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@app.exception_handler(NoResultFound)
async def not_found_exception_handler(request: Request, exc: NoResultFound):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND
    )


from dotenv import load_dotenv
load_dotenv()


logging.basicConfig(level=os.getenv("LOG_LEVEL", logging.INFO))
logger = logging.getLogger("main")


environment = os.getenv("ENVIRONMENT", "dev")  # Default to 'development' if not set
if environment == "dev":
    logger.warning("Running in development mode - allowing CORS for all origins")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
