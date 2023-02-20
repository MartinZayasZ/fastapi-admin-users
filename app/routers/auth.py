

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from ..config import security
from .. import crud
from ..dependencies import get_db
from ..config.schemas import UserOut


router = APIRouter(tags=["auth"], prefix="/auth")

@router.post('/login', response_model=security.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email_and_password(db=db, email=form_data.username, password=security.encode_password(form_data.password))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email, "data": {
            "id": user.id,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "role_id": user.role_id
        }}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
