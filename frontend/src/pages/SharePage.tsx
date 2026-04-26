import {API_BASE, api} from '../api/client';
import {useEffect, useState} from 'react';
import {useParams} from 'react-router-dom';

export function SharePage() {
  const {token} = useParams();
  const [data, setData] = useState<any>(null);
  useEffect(() => { if (token) api(`/api/public/share/${token}`).then(setData); }, [token]);

  if (!data) return <section className='card'>Loading...</section>;
  if (data.type === 'track') {
    return <section className='card'><h2>{data.track?.title}</h2>
      {data.allow_stream && <audio controls src={`${API_BASE}/api/public/share/${token}/stream`} />}
      {data.allow_download && <a href={`${API_BASE}/api/public/share/${token}/download`}>Скачать</a>}
    </section>;
  }
  return <section className='card'><h2>Playlist share</h2><div>{data.playlist?.title}</div></section>;
}
