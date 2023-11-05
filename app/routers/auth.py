from fastapi import Depends, APIRouter, HTTPException, status
from pydantic import EmailStr
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..utils import verify_password

router = APIRouter(tags=["Authentication"])


# def authenticate_user(
#     user_email: EmailStr, password: str, db: Session = Depends(get_db)
# ) -> bool:
#     user_password = (
#         db.query(models.User).filter(models.User.email == user_email).first().password
#     )
#     return verify_password(password, user_password)


def authenticate_user(user_email: str, user_password: str, db: Session) -> bool:
    try:
        password = (
            db.query(models.User)
            .filter(models.User.email == user_email)
            .first()
            .password
        )
        if verify_password(user_password, password):
            return True
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
            )
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )


@router.post("/login")
async def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    authenticate_user(user.email, user.password, db)
