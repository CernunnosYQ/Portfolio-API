from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from schemas.user import CreateUser
from db.session import get_db
from db.crud.user import create_new_user

router = APIRouter()


@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user
