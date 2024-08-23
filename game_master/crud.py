from sqlalchemy.orm import Session
from game_master.models import ServerData


# Function to create a new game session and store it in the database
def create_game(db: Session, session_id: str, number: int):
    server_data = ServerData(id=session_id, number=number, guesses=[])
    db.add(server_data)
    db.commit()
    db.refresh(server_data)
    return server_data

def get_game(db: Session, session_id: str):
    return db.query(ServerData).filter(ServerData.id == session_id).first()

def update_guesses(db: Session, server_data: ServerData, guess: int):
    server_data.guesses.append(guess)
    db.commit()
    db.refresh(server_data)
    return server_data
