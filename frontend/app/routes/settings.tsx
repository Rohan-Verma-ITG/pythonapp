import { Card, FormLayout, Page, TextField } from '@shopify/polaris';

export default function SettingsPage() {
  return (
    <Page title="Settings">
      <Card>
        <FormLayout>
          <TextField label="OpenAI API Key" value="" onChange={() => {}} autoComplete="off" />
          <TextField label="Auto reply mode" value="suggestion" onChange={() => {}} autoComplete="off" />
        </FormLayout>
      </Card>
    </Page>
  );
}
