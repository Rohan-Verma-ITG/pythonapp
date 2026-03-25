from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.models.entities import Message, MessageRole
from backend.schemas.common import AIReplyRequest
from backend.services.ai_service import generate_suggestion


router = APIRouter(prefix='/ai', tags=['ai'])


@router.post('/suggest-reply')
def suggest_reply(payload: AIReplyRequest, db: Session = Depends(get_db)):
    suggestion = generate_suggestion(db, payload.conversation_id, payload.message)
    return {'suggestion': suggestion}


@router.post('/auto-reply')
def auto_reply(payload: AIReplyRequest, db: Session = Depends(get_db)):
    suggestion = generate_suggestion(db, payload.conversation_id, payload.message)
    msg = Message(conversation_id=payload.conversation_id, role=MessageRole.BOT, body=suggestion)
    db.add(msg)
    db.commit()
    return {'sent': True, 'reply': suggestion}
