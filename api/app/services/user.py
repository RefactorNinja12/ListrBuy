from app.repository.user import UserRepository
from app.services.auth import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse,UserNewPassword, UserPassword
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


class UserService: 
    user_repo = UserRepository()
    def register(self, request: UserCreate, db: Session) -> UserResponse: 
        user = self.user_repo.get_by_email(db, request.email)
        if user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registed"
                                )
        new_user = User(
            email = request.email,
            hashed_password = hash_password(request.password)
            )
        return self.user_repo.create(db, new_user)

    def password_change(self,db: Session,password: UserNewPassword, user: User)-> UserResponse:
       
        isVerfied = verify_password(password.old_password, user.hashed_password)
        if isVerfied is False:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Password is not valid"
            ) 
        new_hashed_password = hash_password(password.new_password)
        user.hashed_password = new_hashed_password
        return self.user_repo.update(db, user)
    
    def delete(self, db:Session, password: UserPassword, user: User) -> None:
        isVerfied = verify_password(password.password, user.hashed_password) 
        if isVerfied is False:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Password is not valid"
            )
        self.user_repo.delete(db, user)

    


        


