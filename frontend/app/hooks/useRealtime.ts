import { useEffect } from 'react';

export function useRealtime(shopId: number, onMessage: (payload: any) => void) {
  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/chat/${shopId}`);
    ws.onmessage = (evt) => onMessage(JSON.parse(evt.data));
    return () => ws.close();
  }, [shopId, onMessage]);
}
