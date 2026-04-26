import {useEffect, useState} from 'react';
import {Link} from 'react-router-dom';
import {api} from '../api/client';
import {LocalStatus} from '../types';

export function DashboardPage() {
  const [status, setStatus] = useState<LocalStatus | null>(null);

  useEffect(() => {
    api<LocalStatus>('/api/local/status').then(setStatus);
  }, []);

  return (
    <section className='card'>
      <h2>Dashboard</h2>
      {status && (
        <>
          <p>Режим: {status.mode}</p>
          <p>Сервер: {status.status}</p>
          <p>Локальных треков: {status.tracks_count}</p>
          <p>Источников друзей: {status.friend_storages_count}</p>
          <p>Публичных ссылок: {status.share_links_count}</p>
        </>
      )}
      <div className='row'>
        <Link to='/tracks'>Загрузить трек</Link>
        <Link to='/sources'>Добавить источник</Link>
        <Link to='/links'>Создать ссылку</Link>
      </div>
    </section>
  );
}
