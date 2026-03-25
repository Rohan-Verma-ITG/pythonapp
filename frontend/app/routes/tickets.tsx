import { Badge, Card, DataTable, Page } from '@shopify/polaris';

export default function TicketsPage() {
  return (
    <Page title="Tickets">
      <Card>
        <DataTable
          columnContentTypes={['text', 'text', 'text']}
          headings={['ID', 'Status', 'Priority']}
          rows={[["#23", <Badge key="open">Open</Badge>, 'Normal']]}
        />
      </Card>
    </Page>
  );
}
