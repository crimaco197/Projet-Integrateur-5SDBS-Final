from fastapi import FastAPI

app = FastAPI(title="Orchestrator Service")

@app.get("/")
def read_root():
    return {"Hello": "Orchestrator Service"}

