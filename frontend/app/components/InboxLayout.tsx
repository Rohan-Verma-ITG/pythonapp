export function InboxLayout({ children }: { children: React.ReactNode }) {
  return <div style={{ display: 'grid', gridTemplateColumns: '320px 1fr', gap: 16 }}>{children}</div>;
}
