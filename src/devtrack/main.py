from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from .database import create_tables, insert_task, select_tasks


class TaskCreate(BaseModel):
    title: str
    status: str


class TaskResponse(BaseModel):
    id: int
    title: str
    status: str


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


@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate):
    row = insert_task(task.title, task.status)

    if row is None:
        raise RuntimeError("Task was not created")

    return {
        "id": row[0],
        "title": row[1],
        "status": row[2],
    }
