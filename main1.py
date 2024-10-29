from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Data model for a task
class Task(BaseModel):
    id: int
    description: str
    completed: bool = False

# In-memory storage for tasks
todo_list: List[Task] = []

@app.post("/tasks/", response_model=Task)
def add_task(task: Task):
    todo_list.append(task)
    return task

@app.delete("/tasks/{task_id}")
def remove_task(task_id: int):
    for task in todo_list:
        if task.id == task_id:
            todo_list.remove(task)
            return {"message": f"Task '{task.description}' removed successfully."}
    raise HTTPException(status_code=404, detail="Task not found")

@app.patch("/tasks/{task_id}/complete")
def mark_completed(task_id: int):
    for task in todo_list:
        if task.id == task_id:
            task.completed = True
            return {"message": f"Task '{task.description}' marked as completed."}
    raise HTTPException(status_code=404, detail="Task not found")

@app.get("/tasks/", response_model=List[Task])
def view_tasks():
    return todo_list

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)