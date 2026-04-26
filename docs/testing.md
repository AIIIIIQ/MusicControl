# Testing checklist

1. `docker compose up --build`.
2. UI открывается на `http://localhost:5173` без login.
3. `GET /api/local/status` возвращает `single_owner` и `local_owner`.
4. Upload/stream/download треков работают.
5. Cover upload + `GET /api/tracks/{id}/cover` работают.
6. Share-link открывается через `/share/:token`.
7. Friend storage check показывает status/ping/speed.
8. Sync catalog наполняет remote cache.
9. Remote stream/download работают.
10. Playlists CRUD и share-link на playlist работают.
11. `NODE_REQUIRE_TOKEN=true` блокирует node protected routes без токена.
