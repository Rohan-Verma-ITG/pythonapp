from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.models.entities import Conversation, Message, MessageRole
from backend.schemas.common import MessageCreate
from backend.services.automation import apply_message_rules
from backend.services.realtime import manager


router = APIRouter(prefix='/messages', tags=['messages'])


@router.post('')
async def send_message(payload: MessageCreate, shop_id: int, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == payload.conversation_id, Conversation.shop_id == shop_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail='Conversation not found')

    message = Message(
        conversation_id=payload.conversation_id,
        role=MessageRole(payload.role),
        body=payload.body,
        channel=payload.channel,
    )
    db.add(message)
    db.commit()
    db.refresh(message)

    await manager.broadcast(shop_id, {'type': 'new_message', 'conversation_id': payload.conversation_id, 'body': payload.body})

    auto_reply = apply_message_rules(db, shop_id=shop_id, message=payload.body)
    if auto_reply:
        auto = Message(conversation_id=payload.conversation_id, role=MessageRole.BOT, body=auto_reply, channel=payload.channel)
        db.add(auto)
        db.commit()
        await manager.broadcast(shop_id, {'type': 'new_message', 'conversation_id': payload.conversation_id, 'body': auto_reply})

    return message
