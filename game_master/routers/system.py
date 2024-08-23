from fastapi import APIRouter, Depends
import socket
from sqlalchemy.orm import Session
from game_master.database import Base, get_db
from game_master.models import ServerData


# Initialize the API router for grouping related endpoints
router = APIRouter()

# Endpoint to check the health status of the service
@router.get("/health")
def health():
    return {"status": "healthy"}

# Endpoint to get the hostname of the server
@router.get("/hostname")
def hostname():
    return {"hostname": socket.gethostname()}

# Endpoint to clear all data from the database
@router.post("/clear-data")
def clear_data(db: Session = Depends(get_db)):
    meta = Base.metadata
    for table in reversed(meta.sorted_tables):
        db.execute(table.delete())
    db.commit()
    return {"message": "All data cleared"}

# Endpoint to retrieve all data from the ServerData table
@router.get("/get-all-data")
def get_all_data(db: Session = Depends(get_db)):
    all_data = db.query(ServerData).all()
    
    if not all_data:
        return {"data": []}
    
    result = []
    for data in all_data:
        result.append({
            "session": data.id,
            "number": data.number,
            #"guesses": data.guesses
        })
    
    return {"data": result}
