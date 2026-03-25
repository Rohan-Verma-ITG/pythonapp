import { Card, IndexTable, Page, Text } from '@shopify/polaris';

export default function CustomersPage() {
  return (
    <Page title="Customers">
      <Card>
        <IndexTable
          resourceName={{ singular: 'customer', plural: 'customers' }}
          itemCount={1}
          headings={[{ title: 'Email' }, { title: 'Name' }]}
          selectable={false}
        >
          <IndexTable.Row id="1" key="1" position={0}>
            <IndexTable.Cell><Text as="span">buyer@example.com</Text></IndexTable.Cell>
            <IndexTable.Cell><Text as="span">Buyer One</Text></IndexTable.Cell>
          </IndexTable.Row>
        </IndexTable>
      </Card>
    </Page>
  );
}
