from fastapi import APIRouter, Path, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import exc

from ..dependencies import get_db
from ..config import schemas
from .. import crud

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[schemas.UserOut]:
    users = crud.get_users(db, skip=skip, limit=limit)
    if not users:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, 
            content={"message": "No hay usuarios registrados"}
        )
    return jsonable_encoder(users)

@router.get("/{id}")
def get_user_by_id(id: int, db: Session = Depends(get_db)) -> schemas.UserOut:
    user = crud.get_user_by_id(db, id=id)
    if not user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, 
            content={"message": "No se encontro el usuario"}
        )
    return jsonable_encoder(user)

@router.post('/')
def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):
    
    user = crud.create_user(user=user, db=db)
    return user

    

@router.put('/{id}')
def update_user(id: int = Path(default=...)):
    pass
