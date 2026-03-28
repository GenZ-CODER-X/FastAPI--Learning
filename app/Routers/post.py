from ..schemas import CreatePost,Post
from .. import database_models,oauth2
from fastapi import Depends,status,HTTPException,Response,APIRouter
from ..database import get_db
from typing import List,Optional
from sqlalchemy.orm import Session
from .. import schemas
from sqlalchemy import func

router=APIRouter()

@router.get("/")
def root():
    return{"message":"Hello World"}

@router.get("/posts",response_model=List[schemas.PostOut])
def get_posts(db:Session=Depends(get_db),limit:int=10,search:Optional[str]=""):
    # cursor.execute("""Select * from posts""")
    # posts=cursor.fetchall()
    posts_query=db.query(database_models.Post).filter(database_models.Post.title.contains(search))  #contains is used when its not compulsory to exsist
    posts=posts_query.limit(limit).all()
    #result=db.query(database_models.Post,func.count(database_models.Vote.post_id).label("votes")).join(database_models.Vote,database_models.Vote.post_id==database_models.Post.id,isouter=True).group_by(database_models.Post.id).all() #By defualt this is left inner join
    return posts

@router.post("/createpost",status_code=status.HTTP_201_CREATED,response_model=Post )
def create_posts(post:CreatePost,db:Session=Depends(get_db),Current_User=Depends(oauth2.get_current_user)):
    #new_post=database_models.Post(title=post.title,content=post.content,published=post.published)
                                #OR#
    new_post_query=database_models.Post(**post.model_dump())
    new_post_query.owner_id=Current_User.id
    db.add(new_post_query)
    db.commit()
    db.refresh(new_post_query)
#     cursor.execute("""
# Insert into posts(title,content,published) values(%s,%s,%s) Returning *""" ,(post.title,post.content,post.published))
#     new_post=cursor.fetchone()
#     conn.commit() 
    return new_post_query
#title str,content str
@router.get("/posts/{id}",response_model=Post)
def get_post(id:int,response:Response,db:Session=Depends(get_db),Current_User=Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts where id=%s""",id,)
    # post=cursor.fetchone()
    post_query=db.query(database_models.Post).filter(database_models.Post.id==id) #We can also use all()
    post=post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post with the id {id} is not found")
    return post

@router.delete("/posts/{id}")
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    Current_User = Depends(oauth2.get_current_user)
):
    post = db.query(database_models.Post).filter(database_models.Post.id == id).first()
    # 1. Check if post exists
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} is not found"
        )
    # 2. Check ownership
    if post.owner_id != Current_User.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this"
        )
    # 3. Delete post
    db.delete(post)
    db.commit()

    return {"message": "Post is deleted successfully"}
@router.put("/posts/{id}",response_model=Post)
def update_post(id:int,update_post:schemas.UpdatePost,db:Session=(Depends(get_db)),Current_User=Depends(oauth2.get_current_user)):
    post_query=db.query(database_models.Post).filter(database_models.Post.id==id)
    post=post_query.first()  
    # cursor.execute("Update posts set title=%s,content=%s,published=%s where id =%s returning *",(post.title,post.content,post.published,id))
    # updated_post=cursor.fetchone()

    #First Check if post exsist
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} is not found")
    # conn.commit()

    #Check the ownership
    if post.owner_id!=Current_User.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not allowed to update this post")

    post_query.update(update_post.model_dump(),synchronize_session=False)
    db.commit()
    return post

@router.post("/like")
def like_post(like_data:schemas.Vote,db:Session=Depends(get_db),Current_User=Depends(oauth2.get_current_user)):
    post_id=like_data.post_id
    post=db.query(database_models.Post).filter(database_models.Post.id==post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {post_id} is not found")
    vote_query=db.query(database_models.Vote).filter(database_models.Vote.user_id==Current_User.id,database_models.Vote.post_id==post_id).first()
    if like_data.vote==1:
        if vote_query is None:
            new_like=database_models.Vote(user_id=Current_User.id,post_id=post_id)
            db.add(new_like)
            db.commit()
            return {"message":"Post is liked successfully","title":post.title,"Posted_by":post.owner.email,"Liked_by":Current_User.id}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Already liked the Post")
    if like_data.vote==0:
        if vote_query is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Post is not liked")
        db.delete(vote_query)
        db.commit()
        return{"message":"Unliked the post","title":post.title,"Posted_by":post.owner.email,"Disliked_by":Current_User.id}
    
    
