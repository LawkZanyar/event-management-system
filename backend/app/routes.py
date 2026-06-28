from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Event, User, Attendee

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── EVENTS ────────────────────────────────────────────

@router.get("/events")
def get_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return [
        {
            "id": e.id,
            "title": e.title,
            "description": e.description,
            "date": e.date,
            "location": e.location,
            "created_by": e.created_by
        }
        for e in events
    ]


@router.get("/events/{event_id}")
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return {
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "date": event.date,
        "location": event.location,
        "created_by": event.created_by
    }


@router.post("/events")
def create_event(event_data: dict, db: Session = Depends(get_db)):
    new_event = Event(
        title=event_data["title"],
        description=event_data["description"],
        date=event_data["date"],
        location=event_data["location"],
        created_by=event_data.get("created_by", None)
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return {"message": "Event created", "event": {
        "id": new_event.id,
        "title": new_event.title,
        "description": new_event.description,
        "date": new_event.date,
        "location": new_event.location,
        "created_by": new_event.created_by
    }}


@router.put("/events/{event_id}")
def update_event(event_id: int, event_data: dict, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event.title = event_data["title"]
    event.description = event_data["description"]
    event.date = event_data["date"]
    event.location = event_data["location"]
    event.created_by = event_data.get("created_by", event.created_by)
    db.commit()
    db.refresh(event)
    return {"message": "Event updated", "event": {
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "date": event.date,
        "location": event.location,
        "created_by": event.created_by
    }}


@router.delete("/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(event)
    db.commit()
    return {"message": "Event deleted"}


# ── USERS ─────────────────────────────────────────────

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [
        {"id": u.id, "name": u.name, "email": u.email, "role": u.role}
        for u in users
    ]


@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name, "email": user.email, "role": user.role}


@router.post("/register")
def register(user_data: dict, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_data["email"]).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(
        name=user_data["name"],
        email=user_data["email"],
        password=user_data["password"],
        role="user"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Registered successfully", "user": {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "role": new_user.role
    }}


@router.post("/login")
def login(user_data: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data["email"]).first()
    if not user or user.password != user_data["password"]:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"message": "Login successful", "user": {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }}


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}


# ── ATTENDEES ─────────────────────────────────────────

@router.get("/events/{event_id}/attendees")
def get_attendees(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return [
        {
            "id": a.id,
            "event_id": a.event_id,
            "name": a.name,
            "email": a.email,
            "registered_at": a.registered_at
        }
        for a in event.attendees
    ]


@router.post("/events/{event_id}/attendees")
def add_attendee(event_id: int, attendee_data: dict, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    new_attendee = Attendee(
        event_id=event_id,
        name=attendee_data["name"],
        email=attendee_data["email"],
        registered_at=attendee_data.get("registered_at", "")
    )
    db.add(new_attendee)
    db.commit()
    db.refresh(new_attendee)
    return {"message": "Attendee added", "attendee": {
        "id": new_attendee.id,
        "event_id": new_attendee.event_id,
        "name": new_attendee.name,
        "email": new_attendee.email,
        "registered_at": new_attendee.registered_at
    }}


@router.delete("/attendees/{attendee_id}")
def delete_attendee(attendee_id: int, db: Session = Depends(get_db)):
    attendee = db.query(Attendee).filter(Attendee.id == attendee_id).first()
    if not attendee:
        raise HTTPException(status_code=404, detail="Attendee not found")
    db.delete(attendee)
    db.commit()
    return {"message": "Attendee removed"}