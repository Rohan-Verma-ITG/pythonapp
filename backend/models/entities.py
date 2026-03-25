from datetime import datetime
from enum import Enum

from sqlalchemy import (
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db.session import Base


class TicketStatus(str, Enum):
    OPEN = 'open'
    PENDING = 'pending'
    CLOSED = 'closed'


class MessageRole(str, Enum):
    CUSTOMER = 'customer'
    AGENT = 'agent'
    BOT = 'bot'


class Shop(Base):
    __tablename__ = 'shops'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    shop_domain: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    access_token: Mapped[str] = mapped_column(String(255))
    installed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    users = relationship('User', back_populates='shop', cascade='all,delete')
    customers = relationship('Customer', back_populates='shop', cascade='all,delete')
    orders = relationship('Order', back_populates='shop', cascade='all,delete')
    conversations = relationship('Conversation', back_populates='shop', cascade='all,delete')
    rules = relationship('AutomationRule', back_populates='shop', cascade='all,delete')


class User(Base):
    __tablename__ = 'users'
    __table_args__ = (Index('ix_users_shop_email', 'shop_id', 'email', unique=True),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    shop_id: Mapped[int] = mapped_column(ForeignKey('shops.id', ondelete='CASCADE'), index=True)
    email: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(120))

    shop = relationship('Shop', back_populates='users')
    assigned_tickets = relationship('Ticket', back_populates='assignee')


class Customer(Base):
    __tablename__ = 'customers'
    __table_args__ = (
        UniqueConstraint('shop_id', 'shopify_customer_id', name='uq_customer_per_shop'),
        Index('ix_customer_shop_email', 'shop_id', 'email'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    shop_id: Mapped[int] = mapped_column(ForeignKey('shops.id', ondelete='CASCADE'), index=True)
    shopify_customer_id: Mapped[str] = mapped_column(String(80), index=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    metadata: Mapped[dict] = mapped_column(JSON, default=dict)

    shop = relationship('Shop', back_populates='customers')
    orders = relationship('Order', back_populates='customer')
    conversations = relationship('Conversation', back_populates='customer')


class Order(Base):
    __tablename__ = 'orders'
    __table_args__ = (
        UniqueConstraint('shop_id', 'shopify_order_id', name='uq_order_per_shop'),
        Index('ix_order_shop_customer', 'shop_id', 'customer_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    shop_id: Mapped[int] = mapped_column(ForeignKey('shops.id', ondelete='CASCADE'), index=True)
    customer_id: Mapped[int | None] = mapped_column(ForeignKey('customers.id', ondelete='SET NULL'), nullable=True)
    shopify_order_id: Mapped[str] = mapped_column(String(80), index=True)
    status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    total_price: Mapped[str | None] = mapped_column(String(50), nullable=True)
    metadata: Mapped[dict] = mapped_column(JSON, default=dict)

    shop = relationship('Shop', back_populates='orders')
    customer = relationship('Customer', back_populates='orders')


class Conversation(Base):
    __tablename__ = 'conversations'
    __table_args__ = (Index('ix_conversation_shop_customer', 'shop_id', 'customer_id'),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    shop_id: Mapped[int] = mapped_column(ForeignKey('shops.id', ondelete='CASCADE'), index=True)
    customer_id: Mapped[int | None] = mapped_column(ForeignKey('customers.id', ondelete='SET NULL'), nullable=True)
    channel: Mapped[str] = mapped_column(String(40), default='shopify_chat')
    subject: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    shop = relationship('Shop', back_populates='conversations')
    customer = relationship('Customer', back_populates='conversations')
    messages = relationship('Message', back_populates='conversation', cascade='all,delete')
    ticket = relationship('Ticket', back_populates='conversation', uselist=False)


class Message(Base):
    __tablename__ = 'messages'
    __table_args__ = (Index('ix_message_conversation_created', 'conversation_id', 'created_at'),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey('conversations.id', ondelete='CASCADE'), index=True)
    role: Mapped[MessageRole] = mapped_column(SAEnum(MessageRole), default=MessageRole.CUSTOMER)
    body: Mapped[str] = mapped_column(Text)
    channel: Mapped[str] = mapped_column(String(40), default='shopify_chat')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    conversation = relationship('Conversation', back_populates='messages')


class Ticket(Base):
    __tablename__ = 'tickets'
    __table_args__ = (Index('ix_ticket_shop_status', 'shop_id', 'status'),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    shop_id: Mapped[int] = mapped_column(ForeignKey('shops.id', ondelete='CASCADE'), index=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey('conversations.id', ondelete='CASCADE'), unique=True)
    assignee_id: Mapped[int | None] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    status: Mapped[TicketStatus] = mapped_column(SAEnum(TicketStatus), default=TicketStatus.OPEN)
    priority: Mapped[str] = mapped_column(String(40), default='normal')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    conversation = relationship('Conversation', back_populates='ticket')
    assignee = relationship('User', back_populates='assigned_tickets')


class AutomationRule(Base):
    __tablename__ = 'automation_rules'
    __table_args__ = (Index('ix_rule_shop_event', 'shop_id', 'event_type'),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    shop_id: Mapped[int] = mapped_column(ForeignKey('shops.id', ondelete='CASCADE'), index=True)
    name: Mapped[str] = mapped_column(String(120))
    event_type: Mapped[str] = mapped_column(String(60))
    conditions: Mapped[dict] = mapped_column(JSON, default=dict)
    actions: Mapped[dict] = mapped_column(JSON, default=dict)
    active: Mapped[bool] = mapped_column(default=True)

    shop = relationship('Shop', back_populates='rules')
