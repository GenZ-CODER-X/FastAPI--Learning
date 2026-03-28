from fastapi import FastAPI,Response,HTTPException,status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

tasks=[]

class Task(BaseModel):
    title:str
    description:str
    completed:bool=False
    priority:Optional[int]=None

app=FastAPI()
@app.get("/")
def root():
    return{"message":"Task Api is running"}

@app.post("/tasks",status_code=status.HTTP_201_CREATED)
def create_task(new_task:Task):
    new_task_dict=new_task.dict()
    new_task_dict["id"]=randrange(1,1000000)
    tasks.append(new_task_dict)


@app.get("/tasks")
def get_task():
    return tasks

@app.get("/tasks/{id}")
def get_task(id:int):
    for task in tasks:
        if task["id"]==id:
            return {"Task details":task}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Task with id {id} is not found!")

@app.delete("/tasks/{id}")
def delete_task(id:int):
    for index,task in enumerate(tasks):
        if task["id"]==id:
            tasks.pop(index)
            return{"message":f"Task with id {id} is deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Task with id {id} is not found!")
    
@app.put("/tasks/{id}")
def update_task(id:int,updated_task:Task):
    for task,index in enumerate(tasks):
        if task["id"]==id:
            update_task_dict=updated_task.dict()
            tasks.append(update_task_dict)
            update_task_dict["id"]=id
            tasks[index]=update_task_dict
            return{"message":f"Task is updated successfully and the new task with id {id} is {update_task_dict}"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Task with id {id} is not found!")
