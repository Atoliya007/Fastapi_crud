from fastapi import FastAPI, HTTPException, Depends, status, Query
from pydantic import BaseModel
from typing import Annotated, Optional
from fastapi_pagination import Page, add_pagination, paginate
from sqlalchemy import select, text
from fastapi_pagination.ext.sqlalchemy import paginate
from database import engine, SessionLocal
from sqlalchemy.orm import Session 
import models, database 
from datetime import datetime
from math import ceil
from models import Post , User
import auth

app=FastAPI()
add_pagination(app)
app.include_router(auth.router)

models.Base.metadata.create_all(bind = engine)

class PostBase(BaseModel):
    title:str
    content:str
    user_id:int
    name:str
    email:str
    age:int
    is_active:bool
    created_at:datetime = None
    updated_at:datetime = None
    gender:str
    deleted:bool

class UserBase(BaseModel):
    username:str

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/posts/", status_code=status.HTTP_201_CREATED)
def create_post(post:PostBase, db: Annotated[Session, Depends(get_db)]):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    return db_post

@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
def read_post(post_id:int, db: Annotated[Session, Depends(get_db)]):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        HTTPException(status_code=404, detail='Post was not found')
    return post

@app.get("/posts")
def getAll(name:str = None, age:int = None,  db: Session = Depends(get_db)): 
    query=db.query(Post).filter(Post.deleted == False)

    if name:
        query = query.filter(Post.name.ilike(f"%{name}%"))
    if age:
        query = query.filter(Post.age == age) 
    
    posts = query.all()

    if not posts:
        raise HTTPException(status_code=404, detail="No items found or item is deleted")
    
    return posts

@app.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
def delete_post(post_id:int, db: db_dependency):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Post was not found')
    
    db_post.deleted = True
    
    updated_item = db.merge(db_post)
    db.commit()
    return{"message": f"Item with id '{post_id}' deleted successfully"}

@app.put("/posts/update/{post_id}", status_code=status.HTTP_200_OK)
def updatePost(post_id:int, post:PostBase, db: db_dependency):
    print(post_id, post)
    print("data",db)
    db_post=db.query(models.Post).filter(models.Post.id == post_id).first()
    # updated = db.merge(post)
    db_post.name = post.name
    db_post.title = post.title
    db_post.content = post.content
    db_post.email = post.email
    db.commit()
    db.refresh(db_post)
    return db_post
   
@app.post("/users/", status_code=status.HTTP_201_CREATED)
def create_user(user:UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()

@app.get("/users/{user_id}",status_code=status.HTTP_200_OK)
def read_user(user_id:int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first() 
    if user is  None:
        raise HTTPException(status_code=404, detail='user not found')
    return user