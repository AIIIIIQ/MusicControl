const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

export async function api<T>(path: string, opts: RequestInit = {}, token?: string): Promise<T> {
  const headers: Record<string,string> = {'Content-Type':'application/json', ...(opts.headers as Record<string,string> || {})};
  if (token) headers.Authorization = `Bearer ${token}`;
  const res = await fetch(`${API_BASE}${path}`, {...opts, headers});
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<T>;
}
export { API_BASE };
