from fastapi import APIRouter, Path, Depends, status, Form
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..config.schemas import UserIn, UserOut, UserUpdate
from ..config.models import User
from .. import crud
from ..config.security import verify_token, encode_password

router = APIRouter(
    prefix="/users", 
    tags=["users"], 
    dependencies=[Depends(verify_token)]
)

@router.get("/")
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[UserOut]:
    users = crud.get_users(db, skip=skip, limit=limit)

    if not users:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, 
            content={"message": "No hay usuarios registrados"}
        )
    return jsonable_encoder(users)

@router.get("/{id}")
async def get_user_by_id(id: int, db: Session = Depends(get_db)) -> UserOut:
    user = crud.get_user_by_id(db, id=id)
    if not user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, 
            content={"message": "No se encontro el usuario"}
        )
    return jsonable_encoder(user)

@router.post('/')
async def create_user(user_in: UserIn, db: Session = Depends(get_db), user: User = Depends(verify_token)):
    try:
        userIn.password = encode_password(user_in.password)
        return crud.create_user(user=user_in, created_by=user.id, db=db)
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=408,
            content={
                "message": "El correo ya se encuentra registrado"
            }
        )


@router.put('/{id}', response_model_exclude_unset=True)
def update_user(*, id: int = Path(default=...), user_to_update: UserUpdate, db: Session = Depends(get_db), user: User = Depends(verify_token)):
    try:
        if user_to_update.password:
            print("cambiando contraseña")
            user_to_update.password = encode_password(user_to_update.password)

        crud.update_user(user=user_to_update, id=id, updated_by=user.id, db=db)
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
