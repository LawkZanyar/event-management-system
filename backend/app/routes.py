
from fastapi import APIRouter, Depends  # pyright: ignore[reportMissingImports]
from typing import Any
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
def get_events(db: Any = Depends(get_db)):

    events = db.query(Event).all()

    print("DATABASE EVENTS:", events)

    return [
        {
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "date": event.date,
            "location": event.location
        }
        for event in events
    ]


@router.post("/events")
def create_event(event: dict, db: Any = Depends(get_db)):

    new_event = Event(**event)

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return {
        "id": new_event.id,
        "title": new_event.title,
        "description": new_event.description,
        "date": new_event.date,
        "location": new_event.location
    }


@router.get("/events/{id}")
def get_event(id:int, db:Any=Depends(get_db)):
    return db.query(Event).filter(Event.id==id).first()


@router.delete("/events/{id}")
def delete_event(id:int, db:Any=Depends(get_db)):
    event=db.query(Event).filter(Event.id==id).first()
    db.delete(event)
    db.commit()
    return {"message":"deleted"}
