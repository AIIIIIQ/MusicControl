from datetime import datetime

from pydantic import BaseModel


class Message(BaseModel):
    message: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class UserOut(BaseModel):
    id: int
    username: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True


class SetupRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class InviteCreate(BaseModel):
    role: str = 'user'
    expires_at: datetime | None = None


class RegisterByInviteRequest(BaseModel):
    code: str
    username: str
    password: str


class PlaylistCreate(BaseModel):
    title: str
    description: str | None = None


class PlaylistTrackAdd(BaseModel):
    track_id: int


class ShareLinkCreate(BaseModel):
    target_type: str
    target_id: int
    allow_stream: bool = True
    allow_download: bool = False
    expires_at: datetime | None = None


class FriendStorageCreate(BaseModel):
    title: str
    base_url: str
    access_token: str | None = None


class FriendStorageUpdate(BaseModel):
    title: str
    base_url: str
    access_token: str | None = None


class SyncRoomCreate(BaseModel):
    title: str


class SyncStateUpdate(BaseModel):
    current_track_id: int | None = None
    current_remote_track_id: int | None = None
    position_seconds: float = 0
    is_playing: bool = False


class SettingsUpdate(BaseModel):
    theme: str
