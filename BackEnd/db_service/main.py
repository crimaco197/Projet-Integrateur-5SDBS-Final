from fastapi import FastAPI
from database import Base, engine
from routers import router
from codecarbon import EmissionsTracker

tracker = EmissionsTracker()
tracker.start() 

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Database Microservice")

app.include_router(router, prefix="/reliability", tags=["reliability"])

tracker.stop()