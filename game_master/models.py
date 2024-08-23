from sqlalchemy import Column, Integer, String, JSON
from game_master.database import Base

# Define the ServerData model, which represents the "servers_data" table in the database
class ServerData(Base):
    __tablename__ = "servers_data"

 # Define the columns of the table
    id = Column(String, primary_key=True, index=True)
    number = Column(Integer, index=True)
    guesses = Column(JSON)
    
