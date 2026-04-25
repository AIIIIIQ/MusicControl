import {Link, Navigate, Route, Routes} from 'react-router-dom';
import {useAuth} from './context/AuthContext';
import {PlayerBar} from './components/PlayerBar';
import {LinksPage} from './pages/LinksPage';
import {LoginPage} from './pages/LoginPage';
import {SettingsPage} from './pages/SettingsPage';
import {SourcesPage} from './pages/SourcesPage';
import {TracksPage} from './pages/TracksPage';

export default function App(){
  const {token}=useAuth();
  if(!token) return <LoginPage/>;
  return <div className='layout'><nav><Link to='/tracks'>Треки</Link><Link to='/sources'>Источники</Link><Link to='/links'>Ссылки</Link><Link to='/settings'>Настройки</Link></nav><main><Routes><Route path='/' element={<Navigate to='/tracks'/>}/><Route path='/tracks' element={<TracksPage/>}/><Route path='/sources' element={<SourcesPage/>}/><Route path='/links' element={<LinksPage/>}/><Route path='/settings' element={<SettingsPage/>}/></Routes></main><PlayerBar/></div>
}
