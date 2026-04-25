from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Invite, Role, Setting, User
from app.schemas.common import (
    LoginRequest,
    RegisterByInviteRequest,
    SetupRequest,
    TokenResponse,
    UserOut,
)
from app.utils.deps import get_current_user
from app.utils.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix='/api/auth', tags=['auth'])


@router.post('/setup', response_model=TokenResponse)
def setup(payload: SetupRequest, db: Session = Depends(get_db)):
    if db.query(User).count() > 0:
        raise HTTPException(status_code=400, detail='Setup already completed')
    user = User(username=payload.username, password_hash=hash_password(payload.password), role=Role.admin)
    db.add(user)
    db.flush()
    db.add(Setting(user_id=user.id, theme='dark'))
    db.commit()
    token = create_access_token(user.username, str(user.role))
    return TokenResponse(access_token=token)


@router.post('/register-by-invite', response_model=TokenResponse)
def register_by_invite(payload: RegisterByInviteRequest, db: Session = Depends(get_db)):
    invite = db.query(Invite).filter(Invite.code == payload.code).first()
    if not invite:
        raise HTTPException(status_code=404, detail='Invite not found')
    if invite.used_at:
        raise HTTPException(status_code=400, detail='Invite already used')
    if invite.expires_at and invite.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail='Invite expired')
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=400, detail='Username exists')

    user = User(username=payload.username, password_hash=hash_password(payload.password), role=invite.role)
    invite.used_at = datetime.utcnow()
    db.add(user)
    db.flush()
    db.add(Setting(user_id=user.id, theme='dark'))
    db.commit()
    return TokenResponse(access_token=create_access_token(user.username, str(user.role)))


@router.post('/login', response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    return TokenResponse(access_token=create_access_token(user.username, str(user.role)))


@router.get('/me', response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
