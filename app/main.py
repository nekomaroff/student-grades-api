from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Student Grades API")


@app.get("/")
def healthcheck():
    return {"status": "ok"}


app.include_router(router)