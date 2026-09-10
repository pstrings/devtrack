from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "DevTrack API is running."
    }


@app.get("/tasks")
def get_tasks():
    return [
        {
            "id": 1,
            "title": "Learn Docker",
            "status": "in_progress"
        },
        {
            "id": 2,
            "title": "Learn Kubernetes",
            "status": "todo"
        }
    ]
