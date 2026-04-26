import {FormEvent, useEffect, useState} from 'react';
import {API_BASE, api} from '../api/client';

export function SourcesPage() {
  const [items, setItems] = useState<any[]>([]);
  const [remoteTracks, setRemoteTracks] = useState<any[]>([]);
  const [selectedStorage, setSelectedStorage] = useState<number | null>(null);
  const [title, setTitle] = useState('Друг');
  const [base_url, setBase] = useState('http://localhost:8000');
  const [access_token, setToken] = useState('');

  const load = () => api<any[]>('/api/friend-storages').then(setItems);
  useEffect(() => { load(); }, []);

  const add = async (e: FormEvent) => {
    e.preventDefault();
    await api('/api/friend-storages', {method: 'POST', body: JSON.stringify({title, base_url, access_token: access_token || null})});
    load();
  };

  return <section className='card'><h2>Источники друзей</h2>
    <form onSubmit={add}><input value={title} onChange={e=>setTitle(e.target.value)}/><input value={base_url} onChange={e=>setBase(e.target.value)}/><input value={access_token} onChange={e=>setToken(e.target.value)} placeholder='node token (optional)'/><button>Добавить</button></form>
    {items.map(i=><div key={i.id} className='card'>
      <div>{i.title} — {i.base_url}</div>
      <div>status: {i.status} | ping: {i.last_ping_ms?.toFixed?.(1) || '-'} ms | speed: {i.last_speed_mbps?.toFixed?.(2) || '-'} Mbps</div>
      <div>cached tracks: {i.cached_tracks_count || 0} | last checked: {i.last_checked_at || '-'} {i.last_error ? `| error: ${i.last_error}` : ''}</div>
      <div className='row'>
        <button onClick={async()=>{await api(`/api/friend-storages/${i.id}/check`,{method:'POST'}); load();}}>Проверить</button>
        <button onClick={async()=>{await api(`/api/friend-storages/${i.id}/sync-catalog`,{method:'POST'}); load();}}>Синхронизировать каталог</button>
        <button onClick={async()=>{const tracks=await api<any[]>(`/api/friend-storages/${i.id}/tracks`); setSelectedStorage(i.id); setRemoteTracks(tracks);}}>Открыть треки</button>
        <button onClick={async()=>{await api(`/api/friend-storages/${i.id}`,{method:'DELETE'}); load();}}>Удалить</button>
      </div>
    </div>)}

    {selectedStorage && <div className='card'><h3>Треки источника #{selectedStorage}</h3>
      {remoteTracks.map(t=><div key={t.id} className='row'>
        <span>{t.title} / {t.artist || '-'} / {t.format || '-'} / {t.size_bytes || 0}</span>
        <audio controls src={`${API_BASE}/api/friend-storages/${selectedStorage}/tracks/${t.remote_track_id}/stream`}/>
        {t.can_download && <button onClick={()=>api(`/api/friend-storages/${selectedStorage}/tracks/${t.remote_track_id}/download`,{method:'POST'})}>Скачать</button>}
      </div>)}
    </div>}
  </section>;
}
