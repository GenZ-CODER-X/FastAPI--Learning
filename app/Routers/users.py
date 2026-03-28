from ..schemas import User_Create,UserOut
from fastapi import status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from ..hashing import hash_password
from .. import database_models
from .. import oauth2

router=APIRouter()

@router.post('/user',status_code=status.HTTP_201_CREATED,response_model=UserOut)
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

@router.get('/user/{id}',response_model=UserOut)
def get_User(id:int,db:Session=Depends(get_db)):
    user=db.query(database_models.User).filter(database_models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User is not found')
    return user
    