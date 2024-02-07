from email_validator import validate_email, EmailNotValidError

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.hashing import Hasher
from core.security import create_access_token, validate_access_token
from db.session import get_db
from db.crud.user import get_user_by_email, get_user_by_username

router = APIRouter()


def authenticate_user(email: str, password: str, db: Session):
    try:
        _ = validate_email(email)
        user = get_user_by_email(email=email, db=db)
    except EmailNotValidError:
        user = get_user_by_username(username=email, db=db)
    if not user or not Hasher().verify_password(password, user.password):
        return False
    return user


@router.post("/create/token", status_code=status.HTTP_200_OK)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(
        email=form_data.username, password=form_data.password, db=db
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    validation = validate_access_token(token=token)
    if validation.get("success"):
        username = validation.get("payload").get("sub")
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=validation.get("detail")
        )
    user = get_user_by_username(username=username, db=db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not validate credentials",
        )
    return user
