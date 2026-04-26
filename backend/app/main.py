import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import settings
from app.database import SessionLocal
from app.models import FriendStorage, Setting, ShareLink, Track, User
from app.routers import auth, dev_seed, friend_storages, invites, node_api, playlists, settings as settings_router, share_links, sync_rooms, tracks, users
from app.utils.deps import ensure_local_owner

app = FastAPI(title='MusicControl API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
def startup():
    os.makedirs(settings.music_dir, exist_ok=True)
    os.makedirs(settings.covers_dir, exist_ok=True)
    os.makedirs(settings.downloads_dir, exist_ok=True)

    db: Session = SessionLocal()
    try:
        db.execute(text('SELECT 1'))
        owner = ensure_local_owner(db)
        owner_settings = db.query(Setting).filter(Setting.user_id == owner.id).first()
        if not owner_settings:
            db.add(Setting(user_id=owner.id, theme='dark'))
            db.commit()
    finally:
        db.close()


@app.get('/api/health')
def health():
    db: Session = SessionLocal()
    try:
        users_count = db.query(User).count()
    finally:
        db.close()
    return {'status': 'ok', 'needs_setup': users_count == 0}


@app.get('/api/local/status')
def local_status():
    db: Session = SessionLocal()
    try:
        owner = ensure_local_owner(db)
        return {
            'status': 'ok',
            'mode': 'single_owner',
            'owner': {'id': owner.id, 'username': owner.username},
            'tracks_count': db.query(Track).filter(Track.owner_id == owner.id).count(),
            'friend_storages_count': db.query(FriendStorage).filter(FriendStorage.owner_id == owner.id).count(),
            'share_links_count': db.query(ShareLink).filter(ShareLink.owner_id == owner.id, ShareLink.is_active.is_(True)).count(),
        }
    finally:
        db.close()


app.include_router(auth.router)
app.include_router(invites.router)
app.include_router(tracks.router)
app.include_router(playlists.router)
app.include_router(share_links.router)
app.include_router(friend_storages.router)
app.include_router(node_api.router)
app.include_router(sync_rooms.router)
app.include_router(settings_router.router)
app.include_router(users.router)
app.include_router(dev_seed.router)
