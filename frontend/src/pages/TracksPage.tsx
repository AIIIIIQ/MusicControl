import {FormEvent, useEffect, useState} from 'react';
import {API_BASE, api} from '../api/client';
import {Track} from '../types';

export function TracksPage({onPlay}: {onPlay: (t: Track) => void}) {
  const [tracks, setTracks] = useState<Track[]>([]);
  const [title, setTitle] = useState('');
  const [file, setFile] = useState<File | null>(null);

  const load = () => api<Track[]>('/api/tracks').then(setTracks);
  useEffect(() => {
    load();
  }, []);

  async function upload(e: FormEvent) {
    e.preventDefault();
    if (!file) return;
    const fd = new FormData();
    fd.append('title', title);
    fd.append('artist', '');
    fd.append('album', '');
    fd.append('duration_seconds', '0');
    fd.append('file', file);
    await fetch(`${API_BASE}/api/tracks/upload`, {method: 'POST', body: fd});
    setTitle('');
    setFile(null);
    load();
  }

  async function uploadCover(trackId: number, cover: File | null) {
    if (!cover) return;
    const fd = new FormData();
    fd.append('file', cover);
    await fetch(`${API_BASE}/api/tracks/${trackId}/cover`, {method: 'POST', body: fd});
    load();
  }

  return (
    <section className='card'>
      <h2>Треки</h2>
      <form onSubmit={upload}>
        <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder='Название' />
        <input type='file' accept='.mp3,.flac,.wav,.ogg,.m4a' onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <button>Загрузить</button>
      </form>
      <div className='list'>
        {tracks.map((t) => (
          <div key={t.id} className='row'>
            <img className='cover' src={`${API_BASE}/api/tracks/${t.id}/cover`} onError={(e) => (e.currentTarget.style.opacity = '0.3')} />
            <div>
              {t.title} <small>{t.artist || '—'}</small>
            </div>
            <button onClick={() => onPlay(t)}>Play</button>
            <label>
              Загрузить обложку
              <input type='file' accept='image/*' onChange={(e) => uploadCover(t.id, e.target.files?.[0] || null)} />
            </label>
          </div>
        ))}
      </div>
    </section>
  );
}
