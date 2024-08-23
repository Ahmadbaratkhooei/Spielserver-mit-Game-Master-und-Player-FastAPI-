from fastapi import FastAPI
from game_master.routers import game, system
from game_master.database import engine
from game_master.models import Base


# This will create the tables in the database if they do not already exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title='Game Master')





app.include_router(game.router)
app.include_router(system.router)
