from sqlalchemy.orm import Session

from schemas.user import CreateUser
from db.models.user import User
from core.hashing import Hasher


def create_new_user(user: CreateUser, db: Session):
    user = User(
        username=user.username,
        email=user.email,
        password=Hasher().hash_password(user.password),
        is_active=True,
        is_superuser=False,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
