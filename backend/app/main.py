
from fastapi import FastAPI
from app.database import Base, engine
from app.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Event Management REST API",
    version="1.0"
)

app.include_router(router, prefix="/api")
