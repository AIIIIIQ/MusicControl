import {useEffect, useState} from 'react';
import {api} from '../api/client';
import {useAuth} from '../context/AuthContext';

export function LinksPage(){
  const {token}=useAuth();
  const [links,setLinks]=useState<any[]>([]);
  const [trackId,setTrackId]=useState('1');
  const load=()=>api<any[]>('/api/share-links',{},token||undefined).then(setLinks);
  useEffect(()=>{load();},[]);
  return <section className='card'><h2>Публичные ссылки</h2><div className='row'><input value={trackId} onChange={e=>setTrackId(e.target.value)}/><button onClick={async()=>{await api('/api/share-links',{method:'POST',body:JSON.stringify({target_type:'track',target_id:Number(trackId),allow_stream:true,allow_download:true})},token||undefined); load();}}>Создать</button></div>{links.map(l=><div key={l.id}>{window.location.origin.replace('5173','8000')}/s/{l.token}</div>)}</section>
}
