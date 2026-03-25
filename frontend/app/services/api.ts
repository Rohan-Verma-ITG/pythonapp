export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`http://localhost:8000${path}`);
  if (!res.ok) throw new Error('Request failed');
  return res.json();
}
