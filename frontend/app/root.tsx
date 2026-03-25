import { AppProvider, Page } from '@shopify/polaris';
import polarisStyles from '@shopify/polaris/build/esm/styles.css?url';
import { Links, Meta, Outlet, Scripts, ScrollRestoration } from '@remix-run/react';

export const links = () => [{ rel: 'stylesheet', href: polarisStyles }];

export default function App() {
  return (
    <html>
      <head>
        <Meta />
        <Links />
      </head>
      <body>
        <AppProvider i18n={{}}>
          <Page title="Shopify Helpdesk">
            <Outlet />
          </Page>
        </AppProvider>
        <ScrollRestoration />
        <Scripts />
      </body>
    </html>
  );
}
