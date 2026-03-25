-- PostgreSQL DDL snapshot generated from SQLAlchemy models.
CREATE TABLE shops (
  id SERIAL PRIMARY KEY,
  shop_domain VARCHAR(255) UNIQUE NOT NULL,
  access_token VARCHAR(255) NOT NULL,
  installed_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  shop_id INT NOT NULL REFERENCES shops(id) ON DELETE CASCADE,
  email VARCHAR(255) NOT NULL,
  name VARCHAR(120) NOT NULL
);
CREATE UNIQUE INDEX ix_users_shop_email ON users(shop_id, email);

CREATE TABLE customers (
  id SERIAL PRIMARY KEY,
  shop_id INT NOT NULL REFERENCES shops(id) ON DELETE CASCADE,
  shopify_customer_id VARCHAR(80) NOT NULL,
  email VARCHAR(255),
  name VARCHAR(255),
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  CONSTRAINT uq_customer_per_shop UNIQUE (shop_id, shopify_customer_id)
);
CREATE INDEX ix_customer_shop_email ON customers(shop_id, email);

CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  shop_id INT NOT NULL REFERENCES shops(id) ON DELETE CASCADE,
  customer_id INT REFERENCES customers(id) ON DELETE SET NULL,
  shopify_order_id VARCHAR(80) NOT NULL,
  status VARCHAR(50),
  total_price VARCHAR(50),
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  CONSTRAINT uq_order_per_shop UNIQUE (shop_id, shopify_order_id)
);
CREATE INDEX ix_order_shop_customer ON orders(shop_id, customer_id);

CREATE TABLE conversations (
  id SERIAL PRIMARY KEY,
  shop_id INT NOT NULL REFERENCES shops(id) ON DELETE CASCADE,
  customer_id INT REFERENCES customers(id) ON DELETE SET NULL,
  channel VARCHAR(40) NOT NULL,
  subject VARCHAR(255),
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX ix_conversation_shop_customer ON conversations(shop_id, customer_id);

CREATE TABLE messages (
  id SERIAL PRIMARY KEY,
  conversation_id INT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  role VARCHAR(20) NOT NULL,
  body TEXT NOT NULL,
  channel VARCHAR(40) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX ix_message_conversation_created ON messages(conversation_id, created_at);

CREATE TABLE tickets (
  id SERIAL PRIMARY KEY,
  shop_id INT NOT NULL REFERENCES shops(id) ON DELETE CASCADE,
  conversation_id INT UNIQUE NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  assignee_id INT REFERENCES users(id) ON DELETE SET NULL,
  status VARCHAR(20) NOT NULL,
  priority VARCHAR(40) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX ix_ticket_shop_status ON tickets(shop_id, status);

CREATE TABLE automation_rules (
  id SERIAL PRIMARY KEY,
  shop_id INT NOT NULL REFERENCES shops(id) ON DELETE CASCADE,
  name VARCHAR(120) NOT NULL,
  event_type VARCHAR(60) NOT NULL,
  conditions JSONB NOT NULL DEFAULT '{}'::jsonb,
  actions JSONB NOT NULL DEFAULT '{}'::jsonb,
  active BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE INDEX ix_rule_shop_event ON automation_rules(shop_id, event_type);
