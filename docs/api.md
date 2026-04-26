# API

## Локальный режим
- `GET /api/local/status`
- `GET/POST/PUT/DELETE /api/tracks*`
- `GET/POST /api/playlists*`
- `GET/POST/DELETE /api/share-links*`
- `GET/POST/PUT/DELETE /api/friend-storages*`
- `GET/PUT /api/settings`
- `GET/POST /api/sync-rooms*`

Локальные endpoint'ы работают без Authorization header.

## Публичные ссылки
- `GET /api/public/share/{token}`
- `GET /api/public/share/{token}/stream`
- `GET /api/public/share/{token}/download`
- `GET /s/{token}` -> redirect на `http://localhost:5173/share/{token}`

## Node API
Открытые:
- `GET /api/node/ping`
- `GET /api/node/info`

Опционально защищённые (`NODE_REQUIRE_TOKEN=true`):
- `GET /api/node/catalog`
- `GET /api/node/tracks/{id}`
- `GET /api/node/tracks/{id}/stream`
- `GET /api/node/tracks/{id}/download`
