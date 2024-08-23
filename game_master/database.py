from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Define the database URL. In this case, it's using SQLite and the database file is 'game_master.db'
DATABASE_URL = "sqlite:///./game_master.db"

# Create a SQLAlchemy engine that will interact with the SQLite database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
