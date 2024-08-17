from fastapi import FastAPI

from src.routers import trend

app = FastAPI()

app.include_router(trend.router)
