import secrets
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Playlist, ShareLink, Track, User
from app.schemas.common import ShareLinkCreate
from app.services.streaming import range_response
from app.utils.deps import get_local_owner

router = APIRouter(tags=['share-links'])


@router.get('/api/share-links')
def list_links(user: User = Depends(get_local_owner), db: Session = Depends(get_db)):
    return db.query(ShareLink).filter(ShareLink.owner_id == user.id).all()


@router.post('/api/share-links')
def create_link(payload: ShareLinkCreate, user: User = Depends(get_local_owner), db: Session = Depends(get_db)):
    token = secrets.token_urlsafe(12)
    link = ShareLink(owner_id=user.id, token=token, target_type=payload.target_type, target_id=payload.target_id, allow_stream=payload.allow_stream, allow_download=payload.allow_download, expires_at=payload.expires_at)
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


@router.delete('/api/share-links/{link_id}')
def delete_link(link_id: int, user: User = Depends(get_local_owner), db: Session = Depends(get_db)):
    link = db.query(ShareLink).filter(ShareLink.id == link_id, ShareLink.owner_id == user.id).first()
    if not link:
        raise HTTPException(status_code=404, detail='Not found')
    link.is_active = False
    db.commit()
    return {'message': 'disabled'}


def _link_or_404(token: str, db: Session) -> ShareLink:
    link = db.query(ShareLink).filter(ShareLink.token == token, ShareLink.is_active.is_(True)).first()
    if not link:
        raise HTTPException(status_code=404, detail='Link not found')
    if link.expires_at and link.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail='Link expired')
    return link


@router.get('/api/public/share/{token}')
def public_share(token: str, db: Session = Depends(get_db)):
    link = _link_or_404(token, db)
    if link.target_type == 'track':
        track = db.query(Track).filter(Track.id == link.target_id).first()
        return {'type': 'track', 'allow_stream': link.allow_stream, 'allow_download': link.allow_download, 'track': track}
    playlist = db.query(Playlist).filter(Playlist.id == link.target_id).first()
    return {'type': 'playlist', 'allow_stream': link.allow_stream, 'allow_download': link.allow_download, 'playlist': playlist}


@router.get('/api/public/share/{token}/stream')
def public_stream(token: str, request: Request, db: Session = Depends(get_db)):
    link = _link_or_404(token, db)
    if not link.allow_stream or link.target_type != 'track':
        raise HTTPException(status_code=403, detail='Streaming disabled')
    track = db.query(Track).filter(Track.id == link.target_id).first()
    if not track:
        raise HTTPException(status_code=404, detail='Track missing')
    return range_response(track.file_path, request)


@router.get('/api/public/share/{token}/download')
def public_download(token: str, request: Request, db: Session = Depends(get_db)):
    link = _link_or_404(token, db)
    if not link.allow_download or link.target_type != 'track':
        raise HTTPException(status_code=403, detail='Download disabled')
    track = db.query(Track).filter(Track.id == link.target_id).first()
    if not track:
        raise HTTPException(status_code=404, detail='Track missing')
    return range_response(track.file_path, request, download=True, filename=track.original_filename)


@router.get('/s/{token}')
def public_page(token: str, request: Request):
    return RedirectResponse(url=f'http://localhost:5173/share/{token}', status_code=307)
