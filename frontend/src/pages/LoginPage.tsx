import {FormEvent, useState} from 'react';
import {api} from '../api/client';
import {useAuth} from '../context/AuthContext';

export function LoginPage(){
  const {setToken}=useAuth();
  const [username,setUsername]=useState('admin');
  const [password,setPassword]=useState('admin');
  const [isSetup,setIsSetup]=useState(false);
  const [error,setError]=useState('');
  const [loading,setLoading]=useState(false);

  async function submit(e:FormEvent){
    e.preventDefault();
    setError('');
    setLoading(true);
    try{
      const path=isSetup?'/api/auth/setup':'/api/auth/login';
      const data=await api<{access_token:string}>(path,{method:'POST',body:JSON.stringify({username,password})});
      setToken(data.access_token);
    }catch(err){
      const message = err instanceof Error ? err.message : 'Не удалось выполнить запрос к backend';
      setError(message);
    }finally{
      setLoading(false);
    }
  }

  return <div className='card'><h2>{isSetup?'Первичная настройка':'Вход'}</h2><form onSubmit={submit}><input value={username} onChange={e=>setUsername(e.target.value)} placeholder='username'/><input type='password' value={password} onChange={e=>setPassword(e.target.value)} placeholder='password'/><button disabled={loading}>{loading?'Отправка...':'Отправить'}</button></form>{error && <p className='error'>{error}</p>}<button onClick={()=>setIsSetup(v=>!v)}>{isSetup?'Перейти ко входу':'Первый запуск'}</button></div>
}
