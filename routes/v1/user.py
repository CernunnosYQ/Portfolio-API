from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from email_validator import validate_email, EmailNotValidError

from schemas.user import UserCreate, UserShowPublic
from db.session import get_db
from db.crud.user import create_new_user, get_user_by_email, get_user_by_username

router = APIRouter()


@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user


@router.get("/user/{username}", response_model=UserShowPublic)
def get_user_public_info(username: str, db: Session = Depends(get_db)):
    try:
        _ = validate_email(username)
        user = get_user_by_email(username, db)
    except EmailNotValidError:
        user = get_user_by_username(username, db)

    return UserShowPublic(**user.__dict__)
