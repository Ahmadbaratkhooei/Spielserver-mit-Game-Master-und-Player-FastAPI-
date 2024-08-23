from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from game_master.schemas import GuessInput
from game_master.crud import create_game, get_game, update_guesses
from game_master.database import get_db
import random, uuid


# Initialize the API router for grouping related endpoints
router = APIRouter()

# Endpoint to start a new game
@router.post("/start-game")
def start_game(
    min_number: int = Query(1, description="min_number"),
    max_number: int = Query(1000, description="max_number"),
    db: Session = Depends(get_db)
):
    if min_number >= max_number:
        raise HTTPException(status_code=400)
    
    # Generate a new unique session ID using UUID
    session_id = str(uuid.uuid4())
    # Generate a random number within the specified range
    new_number = random.randint(min_number, max_number)
    create_game(db, session_id, new_number)
    
    return {"message": "New game started", "session_id": session_id, "new_number": new_number}

# Endpoint to submit a guess for a game
@router.post("/submit-guess/{session_id}")
def submit_guess(session_id: str, guess_input: GuessInput, db: Session = Depends(get_db)):
    server_data = get_game(db, session_id)
    if not server_data:
        raise HTTPException(status_code=404, detail="Game not found")
    
    updated_server_data = update_guesses(db, server_data, guess_input.guess)
    
    
    if guess_input.guess == updated_server_data.number:
        return {"result": "won"}
    elif guess_input.guess < updated_server_data.number:
        return {"result": "higher"}
    else:
        return {"result": "lower"}
