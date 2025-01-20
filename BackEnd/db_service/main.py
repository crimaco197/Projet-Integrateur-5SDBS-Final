from fastapi import FastAPI

app = FastAPI(title="DB Service")

@app.get("/")
def read_root():
    return {"Hello": "DB Service"}