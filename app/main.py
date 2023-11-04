from fastapi import FastAPI
from .database import engine, Base
from .routers.post import post_router
from .routers.user import user_router

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(post_router)
app.include_router(user_router)
