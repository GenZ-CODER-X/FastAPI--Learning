from fastapi import APIRouter,Depends,HTTPException,status,Response
from sqlalchemy.orm import Session
from .. import database,oauth2
from ..schemas import UserLogin
from .. import database_models
from ..hashing import verify
from .. import schemas

router=APIRouter(tags=['Authentication'])

@router.post('/login',response_model=schemas.Token)
def login(user_credentials:UserLogin,db:Session=Depends(database.get_db)):

    User=db.query(database_models.User).filter(database_models.User.email==user_credentials.email).first()
    
    if not User:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    
    if not verify(user_credentials.password,User.password):
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    access_token=oauth2.create_acsses_token(data={"user_id":User.id})
    
    #Create and return Token
    return {"access_token":access_token,"token_type":"bearer"}
    
#Next we need to validate the token when user want to accsess next time
    
     