from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Role, User
from app.utils.security import decode_token, hash_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/login')
LOCAL_OWNER_USERNAME = 'local_owner'


def ensure_local_owner(db: Session) -> User:
    owner = db.query(User).filter(User.username == LOCAL_OWNER_USERNAME).first()
    if owner:
        return owner

    owner = User(username=LOCAL_OWNER_USERNAME, password_hash=hash_password('local_owner_disabled_login'), role=Role.admin, is_active=True)
    db.add(owner)
    db.commit()
    db.refresh(owner)
    return owner


def get_local_owner(db: Session = Depends(get_db)) -> User:
    return ensure_local_owner(db)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    user = db.query(User).filter(User.username == payload.get('sub')).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != Role.admin:
        raise HTTPException(status_code=403, detail='Admin role required')
    return user
