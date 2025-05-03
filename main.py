from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(
    title="Task Management API",
    description="A simple FastAPI application for task management",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for Task
class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    completed: bool = False
    created_at: Optional[datetime] = None

# In-memory storage for tasks
tasks = []
current_id = 1

@app.get("/")
async def root():
    """Root endpoint - Welcome message"""
    return {"message": "Welcome to Task Management API"}

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    """Get all tasks"""
    return tasks

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: Task):
    """Create a new task"""
    global current_id
    task.id = current_id
    task.created_at = datetime.now()
    tasks.append(task)
    current_id += 1
    return task

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    """Get a specific task by ID"""
    task = next((task for task in tasks if task.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updated_task: Task):
    """Update a task by ID"""
    task_idx = next((idx for idx, task in enumerate(tasks) if task.id == task_id), None)
    if task_idx is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    updated_task.id = task_id
    updated_task.created_at = tasks[task_idx].created_at
    tasks[task_idx] = updated_task
    return updated_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    """Delete a task by ID"""
    task_idx = next((idx for idx, task in enumerate(tasks) if task.id == task_id), None)
    if task_idx is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    tasks.pop(task_idx)
    return None
