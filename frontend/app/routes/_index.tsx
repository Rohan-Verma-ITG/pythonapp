import { Card, Grid, Text } from '@shopify/polaris';

export default function Dashboard() {
  return (
    <Grid>
      <Grid.Cell columnSpan={{ xs: 6, md: 3, lg: 3, xl: 3 }}>
        <Card>
          <Text as="h2" variant="headingMd">Open Tickets</Text>
          <Text as="p" variant="bodyLg">24</Text>
        </Card>
      </Grid.Cell>
      <Grid.Cell columnSpan={{ xs: 6, md: 3, lg: 3, xl: 3 }}>
        <Card>
          <Text as="h2" variant="headingMd">Active Conversations</Text>
          <Text as="p" variant="bodyLg">58</Text>
        </Card>
      </Grid.Cell>
    </Grid>
  );
}
