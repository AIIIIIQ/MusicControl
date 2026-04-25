import {FormEvent, useEffect, useState} from 'react';
import {API_BASE, api} from '../api/client';
import {useAuth} from '../context/AuthContext';
import {Track} from '../types';

export function TracksPage(){
  const {token}=useAuth();
  const [tracks,setTracks]=useState<Track[]>([]);
  const [title,setTitle]=useState('');
  const [file,setFile]=useState<File|null>(null);
  const [currentUrl,setCurrentUrl]=useState<string>('');

  const load=()=>api<Track[]>('/api/tracks',{},token||undefined).then(setTracks);
  useEffect(()=>{load();},[]);

  async function upload(e:FormEvent){
    e.preventDefault();
    if(!file || !token) return;
    const fd=new FormData(); fd.append('title',title); fd.append('artist',''); fd.append('album',''); fd.append('duration_seconds','0'); fd.append('file',file);
    await fetch(`${API_BASE}/api/tracks/upload`,{method:'POST',headers:{Authorization:`Bearer ${token}`},body:fd});
    setTitle(''); setFile(null); load();
  }

  return <section className='card'><h2>Треки</h2><form onSubmit={upload}><input value={title} onChange={e=>setTitle(e.target.value)} placeholder='Название'/><input type='file' accept='.mp3,.flac,.wav,.ogg,.m4a' onChange={e=>setFile(e.target.files?.[0]||null)}/><button>Загрузить</button></form>
  <div className='list'>{tracks.map(t=><div key={t.id} className='row'><div>{t.title} <small>{t.artist||'—'}</small></div><div><button onClick={async()=>{if(!token) return; const r=await fetch(`${API_BASE}/api/tracks/${t.id}/stream`,{headers:{Authorization:`Bearer ${token}`}}); const b=await r.blob(); setCurrentUrl(URL.createObjectURL(b));}}>Play</button></div></div>)}</div>
  <audio controls src={currentUrl ? currentUrl : undefined}></audio>
  </section>
}
