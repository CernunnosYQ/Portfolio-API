from sqlalchemy.orm import Session

from db.crud.user import create_new_user
from schemas.user import UserCreate

data = {
    "username": "testuser",
    "email": "testuser@test.com",
    "password": "TestUser123456",
}


def create_test_user(db: Session, data: dict = data):
    user = create_new_user(user=UserCreate(**data), db=db)
    return user
