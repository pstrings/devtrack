from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import create_tables, select_tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
def home():
    return {
        "message": "DevTrack API is running."
    }


@app.get("/tasks")
def get_tasks():
    rows = select_tasks()
    return [
        {
            "id": row[0],
            "title": row[1],
            "status": row[2]
        }
        for row in rows
    ]
