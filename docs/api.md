# API

Основные группы:
- Auth: `/api/auth/setup`, `/api/auth/login`, `/api/auth/me`, `/api/auth/register-by-invite`
- Invites: `/api/invites`
- Tracks: CRUD + `/stream` + `/download` + `/cover`
- Playlists: CRUD и треки плейлиста
- Share links: `/api/share-links`, `/api/public/share/{token}`, `/s/{token}`
- Friend storages: check/sync/list/proxy-stream/download
- Node API: `/api/node/info|ping|speedtest|catalog|tracks/*`
- Sync: `/api/sync-rooms`, `/ws/sync-rooms/{id}`
- Settings: `/api/settings`
