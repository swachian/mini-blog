from fastapi import FastAPI
from app.api import post_api

app = FastAPI()

app.include_router(post_api.router)

