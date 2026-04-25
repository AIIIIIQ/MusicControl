import secrets

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Invite, User
from app.schemas.common import InviteCreate
from app.utils.deps import require_admin

router = APIRouter(prefix='/api/invites', tags=['invites'])


@router.post('')
def create_invite(payload: InviteCreate, admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    code = secrets.token_urlsafe(10)
    invite = Invite(code=code, role=payload.role, expires_at=payload.expires_at, created_by_user_id=admin.id)
    db.add(invite)
    db.commit()
    db.refresh(invite)
    return invite


@router.get('')
def list_invites(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    return db.query(Invite).order_by(Invite.created_at.desc()).all()
