import {useEffect, useState} from 'react';
import {api} from '../api/client';
import {useAuth} from '../context/AuthContext';

export function SettingsPage(){
  const {token,setToken}=useAuth();
  const [theme,setTheme]=useState('dark');
  useEffect(()=>{api<any>('/api/settings',{},token||undefined).then(s=>setTheme(s.theme));},[]);
  useEffect(()=>{document.documentElement.dataset.theme=theme;},[theme]);
  return <section className='card'><h2>Настройки</h2><select value={theme} onChange={async e=>{const t=e.target.value; setTheme(t); await api('/api/settings',{method:'PUT',body:JSON.stringify({theme:t})},token||undefined);}}><option value='dark'>Dark</option><option value='light'>Light</option></select><button onClick={()=>setToken(null)}>Выйти</button></section>
}
