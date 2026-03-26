from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.models.entities import Ticket, TicketStatus
from backend.schemas.common import TicketCreate, TicketUpdate


router = APIRouter(prefix='/tickets', tags=['tickets'])
    

@router.get('')
def list_tickets(shop_id: int, db: Session = Depends(get_db)):
    return db.query(Ticket).filter(Ticket.shop_id == shop_id).order_by(Ticket.created_at.desc()).all()


@router.post('')
def create_ticket(payload: TicketCreate, shop_id: int, db: Session = Depends(get_db)):
    ticket = Ticket(shop_id=shop_id, conversation_id=payload.conversation_id, assignee_id=payload.assignee_id, priority=payload.priority)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


@router.get('/{ticket_id}')
def get_ticket(ticket_id: int, shop_id: int, db: Session = Depends(get_db)):
    return db.query(Ticket).filter(Ticket.id == ticket_id, Ticket.shop_id == shop_id).first()


@router.patch('/{ticket_id}')
def update_ticket(ticket_id: int, payload: TicketUpdate, shop_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id, Ticket.shop_id == shop_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail='Not found')
    if payload.status:
        ticket.status = TicketStatus(payload.status)
    if payload.assignee_id is not None:
        ticket.assignee_id = payload.assignee_id
    if payload.priority:
        ticket.priority = payload.priority
    db.commit()
    return ticket


@router.delete('/{ticket_id}')
def delete_ticket(ticket_id: int, shop_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id, Ticket.shop_id == shop_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail='Not found')
    db.delete(ticket)
    db.commit()
    return {'ok': True}
