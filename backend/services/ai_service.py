from openai import OpenAI
from sqlalchemy.orm import Session

from backend.core.config import settings
from backend.models.entities import Conversation


client = OpenAI(api_key=settings.openai_api_key)


def generate_suggestion(db: Session, conversation_id: int, incoming_message: str) -> str:
    convo = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    history = '\n'.join([f"{m.role.value}: {m.body}" for m in (convo.messages[-10:] if convo else [])])

    completion = client.responses.create(
        model=settings.openai_model,
        input=[
            {
                'role': 'system',
                'content': 'You are a helpful support agent. Keep responses concise and empathetic.',
            },
            {
                'role': 'user',
                'content': f'Conversation history:\n{history}\n\nCustomer: {incoming_message}',
            },
        ],
    )
    return completion.output_text
