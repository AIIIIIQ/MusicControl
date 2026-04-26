const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

export async function api<T>(path: string, opts: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = {
    ...(opts.body && !(opts.body instanceof FormData) ? {'Content-Type': 'application/json'} : {}),
    ...((opts.headers as Record<string, string>) || {}),
  };

  const res = await fetch(`${API_BASE}${path}`, {...opts, headers});
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<T>;
}

export {API_BASE};
