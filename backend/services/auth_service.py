from sqlalchemy.orm import Session
from backend.database.models import User
from backend.models.auth import UserCreate, UserLogin, PasswordReset
from backend.utils.security import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException, status

class AuthService:
    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> User:
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email address already registered."
            )
        
        hashed_pwd = get_password_hash(user_data.password)
        new_user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed_pwd,
            role="Admin" if db.query(User).count() == 0 else "User"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def authenticate_user(db: Session, login_data: UserLogin) -> dict:
        user = db.query(User).filter(User.email == login_data.email).first()
        if not user or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials."
            )
        
        token = create_access_token({"sub": str(user.id), "email": user.email, "role": user.role})
        return {"access_token": token, "token_type": "bearer", "user": user}

    @staticmethod
    def reset_password(db: Session, reset_data: PasswordReset) -> bool:
        user = db.query(User).filter(User.email == reset_data.email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
        user.hashed_password = get_password_hash(reset_data.new_password)
        db.commit()
        return True
