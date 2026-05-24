from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, UserNewPassword, UserPassword, Token
from app.services.auth import login, get_current_user
from app.services.user import UserService

router = APIRouter(prefix="/auth", tags=["auth"])
user_service = UserService()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(request: UserCreate, db: Session = Depends(get_db)):
    return user_service.register(request, db)


@router.post("/login", response_model=Token)
def login_user(request: UserLogin, db: Session = Depends(get_db)):
    return login(db, request)


@router.put("/change-password", response_model=UserResponse)
def change_password(
    request: UserNewPassword,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return user_service.password_change(db, request, current_user)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    request: UserPassword,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_service.delete(db, request, current_user)