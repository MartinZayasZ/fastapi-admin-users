from fastapi import APIRouter, Path, Depends, status, Form
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

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
    try:
        return crud.create_user(user=user, db=db)
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=408,
            content={
                "message": "El correo ya se encuentra registrado"
            }
        )


@router.put('/{id}', response_model_exclude_unset=True)
def update_user(*, id: int = Path(default=...), user: schemas.UserUpdate, db: Session = Depends(get_db)):
    try:
        crud.update_user(user=user, id=id, db=db)
        return {
            "message": "El usuario ha sido modificado"
        }
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=409,
            content={
                "message": "El usuario ya se encuentra registrado"
            }
        )
