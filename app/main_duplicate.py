from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from typing import Optional,List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
from . import database_models,schemas
from .database import engine,get_db
from sqlalchemy.orm import Session 
from .schemas import PostBase,CreatePost,Post,User_Create,UserOut
from .hashing import hash_password
#This will allow us to create a table we asked for

database_models.Base.metadata.create_all(bind=engine)#This is a sqlalchemy Command
app=FastAPI()

while True: 
    try:
        conn = psycopg2.connect(host="localhost",database='postgres',user='postgres',password='postgres123',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("DataBase is connected Succesfully")
        break
    except Exception as error:
        print("DataBase is not connected")
        print("Error",error)
        time.sleep(4)


#Test for sqlalchemy
# @app.get("/sqlalchemy")
# def test_post(db:Session=Depends(get_db)):
#     posts=db.query(database_models.Post).all()
#     return{"data":posts}
   
@app.get("/")
def root():
    return{"message":"Hello World"}
@app.get("/posts",response_model=List[Post])
def get_posts(db:Session=Depends(get_db)):
    # cursor.execute("""Select * from posts""")
    # posts=cursor.fetchall()
    posts_query=db.query(database_models.Post)
    posts=posts_query.all()
    return posts

@app.post("/createpost",status_code=status.HTTP_201_CREATED,response_model=Post )
def create_posts(post:CreatePost,db:Session=Depends(get_db)):
    #new_post=database_models.Post(title=post.title,content=post.content,published=post.published)
                                #OR#
    new_post_query=database_models.Post(**post.model_dump())
    db.add(new_post_query)
    db.commit()
    db.refresh(new_post_query)
#     cursor.execute("""
# Insert into posts(title,content,published) values(%s,%s,%s) Returning *""" ,(post.title,post.content,post.published))
#     new_post=cursor.fetchone()
#     conn.commit()
    return new_post_query
#title str,content str
@app.get("/posts/{id}",response_model=Post)
def get_post(id:int,response:Response,db:Session=Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts where id=%s""",id,)
    # post=cursor.fetchone()
    post_query=db.query(database_models.Post).filter(database_models.Post.id==id) #We can also use all()
    post=post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post with the id {id} is not found")
    return post

@app.delete("/posts/{id}")
def delete_post(id:int,db:Session=Depends(get_db)):
    # cursor.execute("DELETE FROM posts where id=%s returning *",(id,))
    # deleted_post=cursor.fetchone()
    # conn.commit()
    post=db.query(database_models.Post).filter(database_models.Post.id==id).first()
    db.delete(post)
    db.commit()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post with id {id} is not found")
    return {"message":"Post is deleted Succesfully"}
@app.put("/posts/{id}",response_model=Post)
def update_post(id:int,post:CreatePost,db:Session=(Depends(get_db))):
    post_query=db.query(database_models.Post).filter(database_models.Post.id==id)
    post=post_query.first()  
    # cursor.execute("Update posts set title=%s,content=%s,published=%s where id =%s returning *",(post.title,post.content,post.published,id))
    # updated_post=cursor.fetchone()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} is not found")
    # conn.commit()
    post_query.update({'title':'Hey this is my updated title','content':'This is my updated content'},synchronize_session=False)
    db.commit()
    return post
@app.post('/user',status_code=status.HTTP_201_CREATED,response_model=UserOut)
def create_user(user_details:User_Create,db:Session=(Depends(get_db))):
    #Hash Password --user.Password
    password=user_details.password[:72]
    hashed_password=hash_password(password)
    user_details.password=hashed_password
    new_user=database_models.User(**user_details.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}',response_model=UserOut)
def get_User(id:int,db:Session=Depends(get_db)):
    user=db.query(database_models.User).filter(database_models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User is not found')
    return user

