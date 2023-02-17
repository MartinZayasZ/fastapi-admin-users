from fastapi import FastAPI

from .config import models
from .config.database import engine

from .routers import users, auth

#models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)