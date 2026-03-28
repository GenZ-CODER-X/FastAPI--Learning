from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

class Post(BaseModel):
    title:str
    published:bool=True
    rating: Optional[int] = None

api=FastAPI()
@api.post("/create_post")
def create_post(post:Post):
    return {"Post":post}

