import {useEffect, useState} from 'react';
import {api} from '../api/client';
import {Playlist, Track} from '../types';

export function PlaylistsPage() {
  const [playlists, setPlaylists] = useState<Playlist[]>([]);
  const [tracks, setTracks] = useState<Track[]>([]);
  const [title, setTitle] = useState('');
  const [selected, setSelected] = useState<number | null>(null);
  const [playlistTracks, setPlaylistTracks] = useState<Track[]>([]);
  const [addTrackId, setAddTrackId] = useState<number>(0);

  const load = async () => {
    const [pls, trs] = await Promise.all([api<Playlist[]>('/api/playlists'), api<Track[]>('/api/tracks')]);
    setPlaylists(pls); setTracks(trs); if (trs[0]) setAddTrackId(trs[0].id);
  };
  useEffect(()=>{load();},[]);

  const openPlaylist = async (id: number) => {
    const data = await api<{playlist: Playlist; tracks: Track[]}>(`/api/playlists/${id}`);
    setSelected(id);
    setPlaylistTracks(data.tracks);
  };

  return <section className='card'><h2>Плейлисты</h2>
    <div className='row'><input value={title} onChange={e=>setTitle(e.target.value)} placeholder='Название плейлиста'/><button onClick={async()=>{await api('/api/playlists',{method:'POST',body:JSON.stringify({title,description:''})}); setTitle(''); load();}}>Создать плейлист</button></div>
    {playlists.map(p=><div className='row' key={p.id}><span>{p.title}</span><button onClick={()=>openPlaylist(p.id)}>Открыть</button><button onClick={async()=>{await api('/api/share-links',{method:'POST',body:JSON.stringify({target_type:'playlist',target_id:p.id,allow_stream:true,allow_download:false,expires_at:null})});}}>Share-link</button></div>)}
    {selected && <div className='card'><h3>Плейлист #{selected}</h3><div className='row'><select value={addTrackId} onChange={e=>setAddTrackId(Number(e.target.value))}>{tracks.map(t=><option key={t.id} value={t.id}>{t.title}</option>)}</select><button onClick={async()=>{await api(`/api/playlists/${selected}/tracks`,{method:'POST',body:JSON.stringify({track_id:addTrackId})}); openPlaylist(selected);}}>Добавить трек</button></div>
      {playlistTracks.map(t=><div className='row' key={t.id}><span>{t.title}</span><button onClick={async()=>{await api(`/api/playlists/${selected}/tracks/${t.id}`,{method:'DELETE'}); openPlaylist(selected);}}>Удалить</button></div>)}
    </div>}
  </section>;
}
