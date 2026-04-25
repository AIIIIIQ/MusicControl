from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import settings as app_settings
from app.database import get_db
from app.models import Setting, User
from app.schemas.common import SettingsUpdate
from app.utils.deps import get_current_user

router = APIRouter(prefix='/api/settings', tags=['settings'])


@router.get('')
def get_settings(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(Setting).filter(Setting.user_id == user.id).first()
    return {'theme': item.theme if item else 'dark', 'node_name': app_settings.node_name, 'music_path': app_settings.music_dir}


@router.put('')
def set_settings(payload: SettingsUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(Setting).filter(Setting.user_id == user.id).first()
    if not item:
        item = Setting(user_id=user.id, theme=payload.theme)
        db.add(item)
    else:
        item.theme = payload.theme
        item.updated_at = datetime.utcnow()
    db.commit()
    return {'message': 'updated'}
