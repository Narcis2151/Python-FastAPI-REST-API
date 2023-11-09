from fastapi import Depends, APIRouter, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from ..utils import verify_password
from ..oauth2 import create_access_token

router = APIRouter(tags=["Authentication"])


@router.post("/login")
async def login_user(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    try:
        user = (
            db.query(models.User)
            .filter(models.User.email == user_credentials.username)
            .first()
        )
        if not verify_password(user_credentials.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials"
            )
        jwt = create_access_token(user_data={"user_id": user.user_id})
        return {"access_token": jwt, "type": "bearer"}
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Credentials"
        )
