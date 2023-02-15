from fastapi import APIRouter

router = APIRouter(tags=["auth"], prefix="/auth")


@router.get('/login')
def login():
    return {}

@router.get('/register')
def register():
    return {}