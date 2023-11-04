from fastapi import FastAPI
from .database import engine, Base
from .routers import post, user

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
