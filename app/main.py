from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
from . import database_models
from .database import engine
from .Routers import post,users,auth
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

#This will allow us to create a table we asked for
database_models.Base.metadata.create_all(bind=engine)
load_dotenv()
app=FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)

#we use this to connect with database using Postgrese
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


