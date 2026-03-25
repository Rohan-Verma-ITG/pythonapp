from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'Shopify Helpdesk API'
    environment: str = 'development'
    secret_key: str = 'replace-me'

    database_url: str = 'postgresql+psycopg2://postgres:postgres@localhost:5432/shopify_helpdesk'
    redis_url: str = 'redis://localhost:6379/0'

    shopify_api_key: str = ''
    shopify_api_secret: str = ''
    shopify_scopes: str = 'read_customers,read_orders,read_products,write_customers,write_orders'
    shopify_app_url: str = 'https://example.com'

    openai_api_key: str = ''
    openai_model: str = 'gpt-4o-mini'


settings = Settings()
