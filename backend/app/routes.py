from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Event


router = APIRouter()


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



# GET ALL EVENTS
@router.get("/events")
def get_events(db: Session = Depends(get_db)):

    events = db.query(Event).all()

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



# GET EVENT BY ID
@router.get("/events/{event_id}")
def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):

    event = db.query(Event).filter(
        Event.id == event_id
    ).first()


    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )


    return {
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "date": event.date,
        "location": event.location
    }



# CREATE EVENT
@router.post("/events")
def create_event(
    event_data: dict,
    db: Session = Depends(get_db)
):

    new_event = Event(
        title=event_data["title"],
        description=event_data["description"],
        date=event_data["date"],
        location=event_data["location"]
    )


    db.add(new_event)
    db.commit()
    db.refresh(new_event)


    return {
        "message": "Event created",
        "event": {
            "id": new_event.id,
            "title": new_event.title,
            "description": new_event.description,
            "date": new_event.date,
            "location": new_event.location
        }
    }



# UPDATE EVENT
@router.put("/events/{event_id}")
def update_event(
    event_id: int,
    event_data: dict,
    db: Session = Depends(get_db)
):

    event = db.query(Event).filter(
        Event.id == event_id
    ).first()


    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )


    event.title = event_data["title"]
    event.description = event_data["description"]
    event.date = event_data["date"]
    event.location = event_data["location"]


    db.commit()
    db.refresh(event)


    return {
        "message": "Event updated",
        "event": {
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "date": event.date,
            "location": event.location
        }
    }



# DELETE EVENT
@router.delete("/events/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db)
):

    event = db.query(Event).filter(
        Event.id == event_id
    ).first()


    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )


    db.delete(event)
    db.commit()


    return {
        "message": "Event deleted"
    }