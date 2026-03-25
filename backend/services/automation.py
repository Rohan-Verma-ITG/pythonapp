from sqlalchemy.orm import Session

from backend.models.entities import AutomationRule


def apply_message_rules(db: Session, shop_id: int, message: str) -> str | None:
    rules = (
        db.query(AutomationRule)
        .filter(AutomationRule.shop_id == shop_id, AutomationRule.event_type == 'message_received', AutomationRule.active.is_(True))
        .all()
    )
    lower = message.lower()
    for rule in rules:
        keyword = rule.conditions.get('keyword')
        if keyword and keyword.lower() in lower:
            return rule.actions.get('reply_text')
    return None
