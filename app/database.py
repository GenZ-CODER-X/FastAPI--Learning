from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from .config import settings

engine=create_engine(settings.database_url)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()

#depedency(This creates a session to db to proceed our APIrequest)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()