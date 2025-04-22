from fastapi import FastAPI
from app.routers import user_router, game_router

app = FastAPI()

app.include_router(user_router.router)
app.include_router(game_router.router)
