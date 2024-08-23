import asyncio
from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel
from typing import List, Dict


# Initialize a FastAPI app with the title 'Player'
app = FastAPI(title='Player')

# Configuration class to game-master
class Config(BaseModel):
    server_a_url: str = "http://game-master:8000"
    number_of_session: int = 1 # Default number of sessions

# Create an instance of the configuration
config = Config()

# Model for the response of a guessing session
class GuessResponse(BaseModel):
    guessed_number: int
    status: str
    session_id: str
    total_guesses: List[Dict[str, str]]

# Function to start a new game session
async def start_new_game():
    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, requests.post, f"{config.server_a_url}/start-game")
        response.raise_for_status()
        session_id = response.json().get("session_id")
        print(f"New game started with new Session: {session_id}")
        return session_id
    except requests.RequestException as e:
        print(f"Failed to start a new game: {e}")
        raise HTTPException(status_code=500, detail="Failed to start a new game")

def post_request(url: str, json_data: dict):
    return requests.post(url, json=json_data)

# Function to guess the number in a session using binary search
async def guess_number(session_id: str):
    low, high = 1, 1000
    total_result = []
    while low <= high:
        guess = (low + high) // 2
        try:
            url = f"{config.server_a_url}/submit-guess/{session_id}"
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, post_request, url, {"guess": guess})
            response.raise_for_status()
            result = response.json().get("result")
            #print(f"server_session:{session_id} result:{result} guess:{guess}")

            total_result.append({
                "result": result,
                "guess": str(guess)   
            })

            if result == "won":
                return GuessResponse(guessed_number=guess, status="correct", total_guesses=total_result, session_id=session_id)
            elif result == "higher":
                low = guess + 1
            else:
                high = guess - 1
        except requests.RequestException as e:
            print(f"Error during guess: {e}")
            raise HTTPException(status_code=500, detail="Error communicating with Game Master")
        
# Endpoint to play the game with the specified number of sessions        
@app.get("/play", response_model=List[GuessResponse])
async def play(number_of_session: int = 1):
    tasks = []
    for _ in range(number_of_session):
        session_id = await start_new_game()
        tasks.append(guess_number(session_id))

    results = await asyncio.gather(*tasks)
    return results

# Endpoint to check the health status of the application
@app.get("/health")
def health():
    return {"status": "healthy"}

# Endpoint to get the hostname of the server
@app.get("/hostname")
def hostname():
    import socket
    return {"hostname": socket.gethostname()}
