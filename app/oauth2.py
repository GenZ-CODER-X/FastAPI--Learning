from jose import JWSError,jwt
from datetime import datetime,timedelta
from . import schemas,database,database_models
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
load_dotenv()

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

# We mainly have 3sections in a JWT token header,payload,signature key

#Secret Key
#Algorith used
#Expiration time of JWT

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_acsses_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id=payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data=schemas.TokenData(id=id)
    except JWSError:
        raise credentials_exception
    return token_data

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(database.get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Couldnt validate User",headers={"WWW-Authenticate":"Bearer"})
    token_data=verify_access_token(token,credentials_exception)
    User=db.query(database_models.User).filter(database_models.User.id==token_data.id).first()
    if User is None:
        return credentials_exception
    return User
    

