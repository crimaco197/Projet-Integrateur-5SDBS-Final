from fastapi import FastAPI
from database import Base, engine
from routers import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DB Service")

app.include_router(router, prefix="/reliability", tags=["reliability"])

@app.get("/")
def read_root():
    return {"Hello": "DB Service"}






