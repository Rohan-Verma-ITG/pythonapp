import { useEffect, useState } from 'react';
import { Button, Card, InlineGrid, Text, TextField } from '@shopify/polaris';

export default function InboxPage() {
  const [messages, setMessages] = useState<string[]>([]);
  const [draft, setDraft] = useState('');

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/chat/1');
    ws.onmessage = (evt) => {
      const data = JSON.parse(evt.data);
      if (data.type === 'new_message') setMessages((prev) => [...prev, data.body]);
    };
    return () => ws.close();
  }, []);

  return (
    <InlineGrid columns={['oneThird', 'twoThirds']}>
      <Card>
        <Text as="h3" variant="headingSm">Conversations</Text>
        <Text as="p">Customer #1234</Text>
      </Card>
      <Card>
        <Text as="h3" variant="headingSm">Chat Window</Text>
        {messages.map((m, idx) => <Text as="p" key={idx}>{m}</Text>)}
        <TextField label="Message" autoComplete="off" value={draft} onChange={setDraft} />
        <Button variant="primary">Send</Button>
        <Button>AI Suggestion</Button>
      </Card>
    </InlineGrid>
  );
}
