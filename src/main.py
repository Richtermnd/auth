import logging

from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles

from . import auth

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:\t%(name)s-%(asctime)s-%(message)s'
    )

app = FastAPI()
app.include_router(auth.router.router)