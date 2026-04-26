import {useEffect, useState} from 'react';
import {api} from '../api/client';
import {ShareLink, Track} from '../types';

export function LinksPage() {
  const [links, setLinks] = useState<ShareLink[]>([]);
  const [tracks, setTracks] = useState<Track[]>([]);
  const [trackId, setTrackId] = useState<number>(0);
  const [allowStream, setAllowStream] = useState(true);
  const [allowDownload, setAllowDownload] = useState(false);
  const [expiry, setExpiry] = useState('never');

  const load = async () => {
    const [l, t] = await Promise.all([api<ShareLink[]>('/api/share-links'), api<Track[]>('/api/tracks')]);
    setLinks(l);
    setTracks(t);
    if (!trackId && t[0]) setTrackId(t[0].id);
  };

  useEffect(() => {
    load();
  }, []);

  const toExpiresAt = () => {
    if (expiry === 'never') return null;
    const now = Date.now();
    const map: Record<string, number> = {h1: 3600e3, d1: 86400e3, d7: 7 * 86400e3};
    return new Date(now + map[expiry]).toISOString();
  };

  return (
    <section className='card'>
      <h2>Публичные ссылки</h2>
      <div className='row'>
        <select value={trackId} onChange={(e) => setTrackId(Number(e.target.value))}>
          {tracks.map((t) => (
            <option key={t.id} value={t.id}>{t.title}</option>
          ))}
        </select>
        <label><input type='checkbox' checked={allowStream} onChange={(e) => setAllowStream(e.target.checked)} />разрешить прослушивание</label>
        <label><input type='checkbox' checked={allowDownload} onChange={(e) => setAllowDownload(e.target.checked)} />разрешить скачивание</label>
        <select value={expiry} onChange={(e) => setExpiry(e.target.value)}>
          <option value='never'>бессрочная</option>
          <option value='h1'>1 час</option>
          <option value='d1'>1 день</option>
          <option value='d7'>7 дней</option>
        </select>
        <button onClick={async () => {
          await api('/api/share-links', {method: 'POST', body: JSON.stringify({target_type: 'track', target_id: trackId, allow_stream: allowStream, allow_download: allowDownload, expires_at: toExpiresAt()})});
          load();
        }}>Создать ссылку</button>
      </div>
      {links.map((l) => {
        const url = `${window.location.origin}/share/${l.token}`;
        return <div className='row' key={l.id}><span>{url}</span><button onClick={() => navigator.clipboard.writeText(url)}>Копировать</button><button onClick={async()=>{await api(`/api/share-links/${l.id}`,{method:'DELETE'});load();}}>Отключить</button></div>;
      })}
    </section>
  );
}
