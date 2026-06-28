from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    password = Column(String(100))
    role = Column(String(20))

    events = relationship("Event", back_populates="creator")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(Text)
    date = Column(String(50))
    location = Column(String(100))
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    creator = relationship("User", back_populates="events")
    attendees = relationship("Attendee", back_populates="event")


class Attendee(Base):
    __tablename__ = "attendees"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    name = Column(String(100))
    email = Column(String(100))
    registered_at = Column(String(50))

    event = relationship("Event", back_populates="attendees")