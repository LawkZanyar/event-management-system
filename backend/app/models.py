
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.database import Base

class Event(Base):
    __tablename__="events"

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(Text)
    date = Column(String(50))
    location = Column(String(100))
