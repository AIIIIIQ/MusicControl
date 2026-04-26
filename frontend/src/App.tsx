import {Link, Navigate, Route, Routes} from 'react-router-dom';
import {useState} from 'react';
import {PlayerBar} from './components/PlayerBar';
import {DashboardPage} from './pages/DashboardPage';
import {LinksPage} from './pages/LinksPage';
import {PlaylistsPage} from './pages/PlaylistsPage';
import {SettingsPage} from './pages/SettingsPage';
import {SharePage} from './pages/SharePage';
import {SourcesPage} from './pages/SourcesPage';
import {TracksPage} from './pages/TracksPage';
import {Track} from './types';

export default function App() {
  const [currentTrack, setCurrentTrack] = useState<Track | null>(null);

  return (
    <div className='layout'>
      <nav>
        <Link to='/'>Главная</Link>
        <Link to='/tracks'>Треки</Link>
        <Link to='/sources'>Источники</Link>
        <Link to='/links'>Ссылки</Link>
        <Link to='/playlists'>Плейлисты</Link>
        <Link to='/settings'>Настройки</Link>
      </nav>
      <main>
        <Routes>
          <Route path='/' element={<DashboardPage />} />
          <Route path='/tracks' element={<TracksPage onPlay={setCurrentTrack} />} />
          <Route path='/sources' element={<SourcesPage />} />
          <Route path='/links' element={<LinksPage />} />
          <Route path='/playlists' element={<PlaylistsPage />} />
          <Route path='/settings' element={<SettingsPage />} />
          <Route path='/share/:token' element={<SharePage />} />
          <Route path='*' element={<Navigate to='/' />} />
        </Routes>
      </main>
      <PlayerBar currentTrack={currentTrack} />
    </div>
  );
}
