import os
import shutil
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import Track, User
from app.services.streaming import range_response
from app.utils.deps import get_local_owner

router = APIRouter(prefix='/api/tracks', tags=['tracks'])
ALLOWED_EXT = {'mp3', 'flac', 'wav', 'ogg', 'm4a'}


def _track_or_404(track_id: int, user_id: int, db: Session) -> Track:
    track = db.query(Track).filter(Track.id == track_id, Track.owner_id == user_id).first()
    if not track:
        raise HTTPException(status_code=404, detail='Track not found')
    return track


@router.get('')
def list_tracks(user: User = Depends(get_local_owner), db: Session = Depends(get_db)):
    return db.query(Track).filter(Track.owner_id == user.id).order_by(Track.created_at.desc()).all()


@router.post('/upload')
async def upload_track(
    file: UploadFile = File(...),
    title: str = Form(...),
    artist: str = Form(''),
    album: str = Form(''),
    duration_seconds: int = Form(0),
    source_type: str = Form('upload'),
    user: User = Depends(get_local_owner),
    db: Session = Depends(get_db),
):
    ext = file.filename.split('.')[-1].lower() if '.' in file.filename else ''
    if ext not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail='Unsupported format')

    os.makedirs(settings.music_dir, exist_ok=True)
    storage_name = f'{uuid.uuid4().hex}.{ext}'
    storage_path = os.path.join(settings.music_dir, storage_name)

    with open(storage_path, 'wb') as out:
        shutil.copyfileobj(file.file, out)

    size = os.path.getsize(storage_path)
    track = Track(
        owner_id=user.id,
        title=title,
        artist=artist or None,
        album=album or None,
        duration_seconds=duration_seconds or None,
        file_path=storage_path,
        original_filename=file.filename,
        mime_type=file.content_type or 'application/octet-stream',
        format=ext,
        size_bytes=size,
        source_type=source_type,
        updated_at=datetime.utcnow(),
    )
    db.add(track)
    db.commit()
    db.refresh(track)
    return track


@router.get('/{track_id}')
def get_track(track_id: int, user: User = Depends(get_local_owner), db: Session = Depends(get_db)):
    return _track_or_404(track_id, user.id, db)


@router.put('/{track_id}')
def update_track(track_id: int, payload: dict, user: User = Depends(get_local_owner), db: Session = Depends(get_db)):
    track = _track_or_404(track_id, user.id, db)
    for field in ['title', 'artist', 'album', 'genre', 'duration_seconds']:
        if field in payload:
            setattr(track, field, payload[field])
    track.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(track)
    return track


@router.delete('/{track_id}')
def delete_track(track_id: int, user: User = Depends(get_local_owner), db: Session = Depends(get_db)):
    track = _track_or_404(track_id, user.id, db)
    if os.path.exists(track.file_path):
        os.remove(track.file_path)
    if track.cover_path and os.path.exists(track.cover_path):
        os.remove(track.cover_path)
    db.delete(track)
    db.commit()
    return {'message': 'deleted'}


@router.post('/{track_id}/cover')
async def upload_cover(track_id: int, file: UploadFile = File(...), user: User = Depends(get_local_owner), db: Session = Depends(get_db)):
    track = _track_or_404(track_id, user.id, db)
    os.makedirs(settings.covers_dir, exist_ok=True)
    ext = file.filename.split('.')[-1].lower() if '.' in file.filename else 'jpg'
    path = os.path.join(settings.covers_dir, f'{uuid.uuid4().hex}.{ext}')
    with open(path, 'wb') as out:
        shutil.copyfileobj(file.file, out)
    track.cover_path = path
    track.updated_at = datetime.utcnow()
    db.commit()
    return {'message': 'cover uploaded'}


@router.get('/{track_id}/cover')
def get_cover(track_id: int, user: User = Depends(get_local_owner), db: Session = Depends(get_db)):
    track = _track_or_404(track_id, user.id, db)
    if not track.cover_path or not os.path.exists(track.cover_path):
        raise HTTPException(status_code=404, detail='Cover not found')
    return FileResponse(track.cover_path)


@router.get('/{track_id}/stream')
def stream(track_id: int, request: Request, user: User = Depends(get_local_owner), db: Session = Depends(get_db)):
    track = _track_or_404(track_id, user.id, db)
    return range_response(track.file_path, request)


@router.get('/{track_id}/download')
def download(track_id: int, request: Request, user: User = Depends(get_local_owner), db: Session = Depends(get_db)):
    track = _track_or_404(track_id, user.id, db)
    return range_response(track.file_path, request, download=True, filename=track.original_filename)
