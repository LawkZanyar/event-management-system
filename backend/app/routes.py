
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Event

router = APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/events")
def get_events(db:Session=Depends(get_db)):
    return db.query(Event).all()


@router.post("/events")
def create_event(event:dict, db:Session=Depends(get_db)):
    new_event=Event(**event)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event


@router.get("/events/{id}")
def get_event(id:int, db:Session=Depends(get_db)):
    return db.query(Event).filter(Event.id==id).first()


@router.delete("/events/{id}")
def delete_event(id:int, db:Session=Depends(get_db)):
    event=db.query(Event).filter(Event.id==id).first()
    db.delete(event)
    db.commit()
    return {"message":"deleted"}
