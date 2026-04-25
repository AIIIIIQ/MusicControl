import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.config import settings
from app.database import SessionLocal
from app.models import User
from app.routers import auth, dev_seed, friend_storages, invites, node_api, playlists, settings as settings_router, share_links, sync_rooms, tracks, users

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


@app.get('/api/health')
def health():
    db: Session = SessionLocal()
    try:
        users_count = db.query(User).count()
    finally:
        db.close()
    return {'status': 'ok', 'needs_setup': users_count == 0}


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
