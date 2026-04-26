from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Playlist, PlaylistTrack, Track, User
from app.schemas.common import PlaylistCreate, PlaylistTrackAdd
from app.utils.deps import get_local_owner

router = APIRouter(prefix='/api/playlists', tags=['playlists'])


def _playlist_or_404(pid: int, uid: int, db: Session):
    pl = db.query(Playlist).filter(Playlist.id == pid, Playlist.owner_id == uid).first()
    if not pl:
        raise HTTPException(status_code=404, detail='Playlist not found')
    return pl


@router.get('')
def list_playlists(user: User = Depends(get_local_owner), db: Session = Depends(get_db)):
    return db.query(Playlist).filter(Playlist.owner_id == user.id).all()


@router.post('')
def create_playlist(payload: PlaylistCreate, user: User = Depends(get_local_owner), db: Session = Depends(get_db)):
    pl = Playlist(owner_id=user.id, title=payload.title, description=payload.description)
    db.add(pl)
    db.commit()
    db.refresh(pl)
    return pl


@router.get('/{playlist_id}')
def get_playlist(playlist_id: int, user: User = Depends(get_local_owner), db: Session = Depends(get_db)):
    pl = _playlist_or_404(playlist_id, user.id, db)
    items = db.query(PlaylistTrack, Track).join(Track, PlaylistTrack.track_id == Track.id).filter(PlaylistTrack.playlist_id == pl.id).order_by(PlaylistTrack.position).all()
    return {'playlist': pl, 'tracks': [t for _, t in items]}


@router.post('/{playlist_id}/tracks')
def add_track(playlist_id: int, payload: PlaylistTrackAdd, user: User = Depends(get_local_owner), db: Session = Depends(get_db)):
    _playlist_or_404(playlist_id, user.id, db)
    track = db.query(Track).filter(Track.id == payload.track_id, Track.owner_id == user.id).first()
    if not track:
        raise HTTPException(status_code=404, detail='Track not found')
    pos = db.query(PlaylistTrack).filter(PlaylistTrack.playlist_id == playlist_id).count()
    pt = PlaylistTrack(playlist_id=playlist_id, track_id=payload.track_id, position=pos)
    db.add(pt)
    db.commit()
    return {'message': 'added'}


@router.delete('/{playlist_id}/tracks/{track_id}')
def remove_track(playlist_id: int, track_id: int, user: User = Depends(get_local_owner), db: Session = Depends(get_db)):
    _playlist_or_404(playlist_id, user.id, db)
    pt = db.query(PlaylistTrack).filter(PlaylistTrack.playlist_id == playlist_id, PlaylistTrack.track_id == track_id).first()
    if not pt:
        raise HTTPException(status_code=404, detail='Not found')
    db.delete(pt)
    db.commit()
    return {'message': 'removed'}
