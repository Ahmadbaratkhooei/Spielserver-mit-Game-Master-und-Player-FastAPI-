from pydantic import BaseModel


# Define the GuessInput model using Pydantic's BaseModel
class GuessInput(BaseModel):
    guess: int
