import {FormEvent, useEffect, useState} from 'react';
import {api} from '../api/client';
import {useAuth} from '../context/AuthContext';

export function SourcesPage(){
  const {token}=useAuth();
  const [items,setItems]=useState<any[]>([]);
  const [title,setTitle]=useState('Друг');
  const [base_url,setBase]=useState('http://localhost:8000');
  const load=()=>api<any[]>('/api/friend-storages',{},token||undefined).then(setItems);
  useEffect(()=>{load();},[]);
  const add=async(e:FormEvent)=>{e.preventDefault(); await api('/api/friend-storages',{method:'POST',body:JSON.stringify({title,base_url,access_token:null})},token||undefined); load();}
  return <section className='card'><h2>Источники друзей</h2><form onSubmit={add}><input value={title} onChange={e=>setTitle(e.target.value)}/><input value={base_url} onChange={e=>setBase(e.target.value)}/><button>Добавить</button></form>{items.map(i=><div key={i.id} className='row'><div>{i.title} ({i.status})</div><button onClick={async()=>{await api(`/api/friend-storages/${i.id}/check`,{method:'POST'},token||undefined); load();}}>Проверить</button></div>)}</section>
}
