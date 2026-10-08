from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import Token, UserOut, UserRegister, UserUpdate
from app.security import create_access_token, get_current_user, hash_password, require_admin, verify_password

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user: UserRegister, db: Session = Depends(get_db)):
    """Register a new account. Uses hash_password from security.py so we never save the real password."""
    existing = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already taken")

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        role="user",
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Log in. Uses verify_password to check the password, then create_access_token to hand back a token."""
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token = create_access_token({"user_id": user.id})
    return Token(access_token=access_token)


@router.get("/me", response_model=UserOut)
def get_my_profile(current_user: User = Depends(get_current_user)):
    """Get my own profile. Uses get_current_user from security.py to know who's asking."""
    return current_user


@router.patch("/me", response_model=UserOut)
def update_my_profile(
    updates: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update my own profile. Uses get_current_user to know who I am, and hash_password again if I'm changing my password."""
    if updates.username is not None:
        current_user.username = updates.username
    if updates.email is not None:
        current_user.email = updates.email
    if updates.password is not None:
        current_user.hashed_password = hash_password(updates.password)

    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("", response_model=list[UserOut])
def get_all_users(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    """Get every user. Admin only, uses require_admin from security.py."""
    return db.query(User).all()


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    """Get one user by id. Admin only, uses require_admin from security.py."""
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    """Delete a user. Admin only, uses require_admin from security.py."""
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted"}
