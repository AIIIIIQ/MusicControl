export type Track = {
  id: number;
  title: string;
  artist?: string;
  album?: string;
  format?: string;
  size_bytes?: number;
};

export type Playlist = { id: number; title: string; description?: string };

export type ShareLink = {
  id: number;
  token: string;
  target_type: string;
  target_id: number;
  allow_stream: boolean;
  allow_download: boolean;
  expires_at?: string | null;
  is_active: boolean;
};

export type LocalStatus = {
  status: string;
  mode: string;
  owner: { id: number; username: string };
  tracks_count: number;
  friend_storages_count: number;
  share_links_count: number;
};
