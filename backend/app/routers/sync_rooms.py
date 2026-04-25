from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.database import SessionLocal, get_db
from app.models import SyncRoom, User
from app.schemas.common import SyncRoomCreate, SyncStateUpdate
from app.utils.deps import get_current_user

router = APIRouter(tags=['sync'])
rooms_connections: dict[int, list[WebSocket]] = {}


def _room_or_404(room_id: int, db: Session):
    room = db.query(SyncRoom).filter(SyncRoom.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail='Room not found')
    return room


@router.post('/api/sync-rooms')
def create_room(payload: SyncRoomCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    room = SyncRoom(owner_id=user.id, title=payload.title)
    db.add(room)
    db.commit()
    db.refresh(room)
    return room


@router.get('/api/sync-rooms')
def list_rooms(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(SyncRoom).all()


@router.get('/api/sync-rooms/{room_id}')
def get_room(room_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return _room_or_404(room_id, db)


@router.post('/api/sync-rooms/{room_id}/state')
async def update_state(room_id: int, payload: SyncStateUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    room = _room_or_404(room_id, db)
    if room.owner_id != user.id:
        raise HTTPException(status_code=403, detail='Only owner can update state')
    room.current_track_id = payload.current_track_id
    room.current_remote_track_id = payload.current_remote_track_id
    room.position_seconds = payload.position_seconds
    room.is_playing = payload.is_playing
    room.updated_at = datetime.utcnow()
    db.commit()

    for ws in rooms_connections.get(room_id, []):
        await ws.send_json({'track_id': room.current_track_id, 'remote_track_id': room.current_remote_track_id, 'position_seconds': room.position_seconds, 'is_playing': room.is_playing, 'updated_at': room.updated_at.isoformat()})
    return room


@router.websocket('/ws/sync-rooms/{room_id}')
async def ws_room(websocket: WebSocket, room_id: int):
    await websocket.accept()
    db = SessionLocal()
    try:
        _room_or_404(room_id, db)
        rooms_connections.setdefault(room_id, []).append(websocket)
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        db.close()
        if room_id in rooms_connections and websocket in rooms_connections[room_id]:
            rooms_connections[room_id].remove(websocket)
