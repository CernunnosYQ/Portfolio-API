from sqlalchemy.orm import Session

from schemas.user import UserCreate
from db.models.user import User
from core.hashing import Hasher


def create_new_user(user: UserCreate, db: Session):
    user = User(
        username=user.username,
        email=user.email,
        password=Hasher().hash_password(user.password),
        avatar="",
        description="",
        is_active=True,
        is_superuser=False,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user


def get_user_by_username(username: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    return user
