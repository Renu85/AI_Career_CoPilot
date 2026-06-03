


from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env", override=True)


DATABASE_URL=os.getenv("DATABASE_URL") 

print("ENV loaded:", load_dotenv(".env"))
print("DATABASE_URL:", repr("DATABASE_URL"))

engine  = create_engine(
     DATABASE_URL,
    pool_pre_ping=True,
    
)

SessionLocal = sessionmaker(bind=engine)
Base= declarative_base()





