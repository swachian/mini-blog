from fastapi import FastAPI
from app.controller import post_controller

app = FastAPI(
    title = "Mini Blog API",
    summary = "An application about mongo, es and FastAPI."
)

app.include_router(post_controller.router)

