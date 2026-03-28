from pydantic import BaseModel,EmailStr
from datetime import datetime
#This is called as Schema
# class Post(BaseModel):
#     title:str
#     content:str
#     published: bool =True

class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True

class CreatePost(PostBase):
    pass

class UpdatePost(BaseModel):
    title:str
    content:str

#Schema For user_out of registartion
class UserOut(BaseModel):
    id:int
    email:EmailStr
    class config:
        orm_mode=True


#NOW WE ARE DEFINING SCHEMA FOR RESPONSE TO USER
class Post(PostBase):
    created_at:datetime
    owner_id:int
    owner:UserOut
    class config:
        orm_mode=True
        
class PostOut(BaseModel):
    Post:Post
    votes:int
    class Config:
        from_attributes=True


#user_registartionschema
class User_Create(BaseModel):
     email:EmailStr
     password:str
  
#Schema For user_out of registartion
class UserOut(BaseModel):
    id:int
    email:EmailStr
    class config:
        orm_mode=True
  
#Schema for user login
class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:int


#Schema for liking post
class Vote(BaseModel):
    post_id:int
    vote:int
