import os
import time
from datetime import datetime

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import DownloadHistory, FriendStorage, RemoteTrackCache, User
from app.schemas.common import FriendStorageCreate, FriendStorageUpdate
from app.utils.deps import get_local_owner

router = APIRouter(prefix='/api/friend-storages', tags=['friend-storages'])


def _item_or_404(sid: int, uid: int, db: Session):
    item = db.query(FriendStorage).filter(FriendStorage.id == sid, FriendStorage.owner_id == uid).first()
    if not item:
        raise HTTPException(status_code=404, detail='Source not found')
    return item


def _headers(storage: FriendStorage):
    return {'Authorization': f'Bearer {storage.access_token}'} if storage.access_token else {}


@router.get('')
def list_items(user: User = Depends(get_local_owner), db: Session = Depends(get_db)):
    items = db.query(FriendStorage).filter(FriendStorage.owner_id == user.id).all()
    return [
        {
            **{c.name: getattr(item, c.name) for c in item.__table__.columns},
            'cached_tracks_count': db.query(RemoteTrackCache).filter(RemoteTrackCache.friend_storage_id == item.id).count(),
        }
        for item in items
    ]


@router.post('')
def create_item(payload: FriendStorageCreate, user: User = Depends(get_local_owner), db: Session = Depends(get_db)):
    item = FriendStorage(owner_id=user.id, **payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put('/{storage_id}')
def update_item(storage_id: int, payload: FriendStorageUpdate, user: User = Depends(get_local_owner), db: Session = Depends(get_db)):
    item = _item_or_404(storage_id, user.id, db)
    for k, v in payload.model_dump().items():
        setattr(item, k, v)
    db.commit()
    return item


@router.delete('/{storage_id}')
def delete_item(storage_id: int, user: User = Depends(get_local_owner), db: Session = Depends(get_db)):
    item = _item_or_404(storage_id, user.id, db)
    db.delete(item)
    db.commit()
    return {'message': 'deleted'}


@router.post('/{storage_id}/check')
def check(storage_id: int, user: User = Depends(get_local_owner), db: Session = Depends(get_db)):
    item = _item_or_404(storage_id, user.id, db)
    started = time.perf_counter()
    try:
        with httpx.Client(timeout=10) as client:
            r = client.get(f'{item.base_url}/api/node/ping', headers=_headers(item))
            r.raise_for_status()
            speed = client.get(f'{item.base_url}/api/node/speedtest', headers=_headers(item), timeout=20)
            size = len(speed.content)
        elapsed = max((time.perf_counter() - started), 0.001)
        item.status = 'online'
        item.last_ping_ms = elapsed * 1000
        item.last_speed_mbps = (size * 8 / 1_000_000) / elapsed
        item.last_error = None
    except Exception as e:
        item.status = 'offline'
        item.last_error = str(e)
    item.last_checked_at = datetime.utcnow()
    db.commit()
    return item


@router.post('/{storage_id}/sync-catalog')
def sync_catalog(storage_id: int, user: User = Depends(get_local_owner), db: Session = Depends(get_db)):
    item = _item_or_404(storage_id, user.id, db)
    with httpx.Client(timeout=15) as client:
        r = client.get(f'{item.base_url}/api/node/catalog', headers=_headers(item))
        r.raise_for_status()
        catalog = r.json()
    db.query(RemoteTrackCache).filter(RemoteTrackCache.friend_storage_id == item.id).delete()
    for t in catalog:
        db.add(RemoteTrackCache(friend_storage_id=item.id, remote_track_id=t['id'], title=t['title'], artist=t.get('artist'), album=t.get('album'), duration_seconds=t.get('duration_seconds'), format=t.get('format'), size_bytes=t.get('size_bytes'), can_stream=t.get('can_stream', True), can_download=t.get('can_download', False)))
    item.last_checked_at = datetime.utcnow()
    db.commit()
    return {'count': len(catalog)}


@router.get('/{storage_id}/tracks')
def list_remote_tracks(storage_id: int, user: User = Depends(get_local_owner), db: Session = Depends(get_db)):
    _item_or_404(storage_id, user.id, db)
    return db.query(RemoteTrackCache).filter(RemoteTrackCache.friend_storage_id == storage_id).all()


@router.get('/{storage_id}/tracks/{remote_track_id}/stream')
def stream_remote(storage_id: int, remote_track_id: int, request: Request, user: User = Depends(get_local_owner), db: Session = Depends(get_db)):
    item = _item_or_404(storage_id, user.id, db)
    url = f'{item.base_url}/api/node/tracks/{remote_track_id}/stream'
    headers = _headers(item)
    if request.headers.get('range'):
        headers['Range'] = request.headers['range']
    client = httpx.Client(timeout=30)
    resp = client.stream('GET', url, headers=headers)
    stream = resp.__enter__()
    if stream.status_code >= 400:
        raise HTTPException(status_code=stream.status_code, detail='Remote stream failed')
    out_headers = {'Content-Type': stream.headers.get('content-type', 'audio/mpeg')}
    for h in ['content-range', 'content-length', 'accept-ranges']:
        if h in stream.headers:
            out_headers[h.title()] = stream.headers[h]
    return StreamingResponse(stream.iter_bytes(), status_code=stream.status_code, headers=out_headers)


@router.post('/{storage_id}/tracks/{remote_track_id}/download')
def download_remote(storage_id: int, remote_track_id: int, user: User = Depends(get_local_owner), db: Session = Depends(get_db)):
    item = _item_or_404(storage_id, user.id, db)
    with httpx.Client(timeout=30) as client:
        resp = client.get(f'{item.base_url}/api/node/tracks/{remote_track_id}/download', headers=_headers(item))
        resp.raise_for_status()
        os.makedirs(settings.downloads_dir, exist_ok=True)
        out = os.path.join(settings.downloads_dir, f'remote_{storage_id}_{remote_track_id}.bin')
        with open(out, 'wb') as f:
            f.write(resp.content)
    db.add(DownloadHistory(user_id=user.id, remote_track_id=remote_track_id, friend_storage_id=storage_id))
    db.commit()
    return {'path': out}
