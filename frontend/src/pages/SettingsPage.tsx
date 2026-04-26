import {useEffect, useState} from 'react';
import {api} from '../api/client';

export function SettingsPage() {
  const [theme, setTheme] = useState('dark');
  useEffect(() => { api<any>('/api/settings').then((s) => setTheme(s.theme)); }, []);
  useEffect(() => { document.documentElement.dataset.theme = theme; }, [theme]);
  return <section className='card'><h2>Настройки</h2><select value={theme} onChange={async (e) => { const t = e.target.value; setTheme(t); await api('/api/settings', {method: 'PUT', body: JSON.stringify({theme: t})}); }}><option value='dark'>Dark</option><option value='light'>Light</option></select></section>;
}
