from fastapi import FastAPI
from sqlalchemy import event

from .config import models
from .config.database import engine
from .config.models import User, Role
from .config.seeding import initialize_table

from .routers import users, auth

#models.Base.metadata.drop_all(bind=engine)
#models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MZAYAS - CMS API",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(users.router)

# I set up this event before table creation
event.listen(User.__table__, 'after_create', initialize_table)
event.listen(Role.__table__, 'after_create', initialize_table)

# This will create the DB schema and trigger the "after_create" event
@app.on_event("startup")
def configure():
    print("StartUP Executed!")
    #models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)