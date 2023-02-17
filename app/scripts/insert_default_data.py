import crud
from dependencies import get_db

db = get_db()

superadmin = {
    "firstname": "Admin",
    "lastname": "",
    "email": "mail@example.com",
    "password": "password",
    "role_id": 1
}

crud.create_user(user=superadmin, db=db)