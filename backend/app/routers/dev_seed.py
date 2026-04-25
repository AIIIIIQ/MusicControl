from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import FriendStorage, Role, Track, User
from app.utils.deps import require_admin
from app.utils.security import hash_password

router = APIRouter(prefix='/api/dev', tags=['dev'])


@router.post('/seed')
def seed(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    created = []
    for username in ['demo_user', 'guest1']:
        if not db.query(User).filter(User.username == username).first():
            db.add(User(username=username, password_hash=hash_password('password'), role=Role.user))
            created.append(username)
    db.commit()
    if db.query(FriendStorage).count() == 0:
        db.add(FriendStorage(owner_id=admin.id, title='Friend Localhost', base_url='http://backend:8000', access_token=None, status='unknown'))
    db.commit()
    return {'users_created': created}
