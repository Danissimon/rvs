from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import create_number, get_number, get_max_number
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class IncrementResponse(BaseModel):
    incremented_value: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/increment/", response_model=IncrementResponse)
def increment_number(value: int, db: Session = Depends(get_db)):
    if value < 0:
        raise HTTPException(status_code=400, detail="Number must be a natural number (0 or greater).")

    existing_number = get_number(db, value)
    max_number = get_max_number(db)

    if existing_number:
        logger.error(f"Error: Number {value} has already been processed.")
        raise HTTPException(status_code=400, detail="This number has already been processed.")

    if max_number and value < max_number.value:
        logger.error(f"Error: Number {value} is less than the maximum processed number {max_number.value}.")
        raise HTTPException(status_code=400, detail="The number is less than the last processed number.")

    create_number(db, value)

    return IncrementResponse(incremented_value=value + 1)