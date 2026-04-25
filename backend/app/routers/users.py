from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.utils.deps import require_admin

router = APIRouter(prefix='/api/users', tags=['users'])


@router.get('')
def list_users(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    return db.query(User).all()
