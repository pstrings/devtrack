from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .database import create_tables, delete_task, insert_task, select_task, select_tasks, update_task


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


@app.get("/tasks", response_model=list[TaskResponse])
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


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    row = select_task(task_id)

    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "id": row[0],
        "title": row[1],
        "status": row[2],
    }


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


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task_endpoint(task_id: int, task: TaskCreate):
    row = update_task(task_id, task.title, task.status)

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return {
        "id": row[0],
        "title": row[1],
        "status": row[2],
    }


@app.delete("/tasks/{task_id}", response_model=TaskResponse)
def remove_task(task_id: int):
    row = delete_task(task_id)

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return {
        "id": row[0],
        "title": row[1],
        "status": row[2],
    }
