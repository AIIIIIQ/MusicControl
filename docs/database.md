# База данных

Используются таблицы: users, invites, tracks, playlists, playlist_tracks, share_links, friend_storages, remote_tracks_cache, download_history, play_history, sync_rooms, settings.

Логическая модель:
- Пользователь владеет треками/плейлистами/ссылками/источниками.
- Playlist many-to-many Tracks через playlist_tracks.
- Friend storage кеширует remote catalog.
- Share link указывает на track или playlist.
