from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import Track
from app.services.streaming import range_response

router = APIRouter(prefix='/api/node', tags=['node'])


@router.get('/info')
def info():
    return {'name': settings.node_name, 'description': settings.node_description, 'version': '0.1.0'}


@router.get('/ping')
def ping():
    return {'status': 'ok'}


@router.get('/speedtest')
def speedtest():
    return 'x' * 1_000_000


@router.get('/catalog')
def catalog(db: Session = Depends(get_db)):
    tracks = db.query(Track).all()
    return [
        {
            'id': t.id,
            'title': t.title,
            'artist': t.artist,
            'album': t.album,
            'duration_seconds': t.duration_seconds,
            'format': t.format,
            'size_bytes': t.size_bytes,
            'can_stream': True,
            'can_download': True,
        }
        for t in tracks
    ]


@router.get('/tracks/{track_id}')
def track_meta(track_id: int, db: Session = Depends(get_db)):
    t = db.query(Track).filter(Track.id == track_id).first()
    if not t:
        raise HTTPException(status_code=404, detail='Not found')
    return t


@router.get('/tracks/{track_id}/stream')
def node_stream(track_id: int, request: Request, db: Session = Depends(get_db)):
    t = db.query(Track).filter(Track.id == track_id).first()
    if not t:
        raise HTTPException(status_code=404, detail='Not found')
    return range_response(t.file_path, request)


@router.get('/tracks/{track_id}/download')
def node_download(track_id: int, request: Request, db: Session = Depends(get_db)):
    t = db.query(Track).filter(Track.id == track_id).first()
    if not t:
        raise HTTPException(status_code=404, detail='Not found')
    return range_response(t.file_path, request, download=True, filename=t.original_filename)
