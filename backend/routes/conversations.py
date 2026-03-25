from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.models.entities import Conversation, Message
from backend.schemas.common import ConversationCreate


router = APIRouter(tags=['conversations'])


@router.get('/conversations')
def list_conversations(shop_id: int, db: Session = Depends(get_db)):
    return db.query(Conversation).filter(Conversation.shop_id == shop_id).order_by(Conversation.created_at.desc()).limit(200).all()


@router.post('/conversations')
def create_conversation(payload: ConversationCreate, shop_id: int, db: Session = Depends(get_db)):
    conversation = Conversation(shop_id=shop_id, customer_id=payload.customer_id, channel=payload.channel, subject=payload.subject)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


@router.get('/messages/{conversation_id}')
def list_messages(conversation_id: int, shop_id: int, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.shop_id == shop_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail='Conversation not found')
    return db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at.asc()).all()
