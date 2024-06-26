from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
import models
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np

app = FastAPI()
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"]   # Allow all headers
)

# Load the pre-trained model
model = joblib.load('model.pkl')

# Pydantic model
class TransactionBase(BaseModel):
    name: str
    men: bool
    age: int
    height: float
    
# Pydantic model for prediction input
class PredictionInput(BaseModel):
    men: bool
    height: float

# Pydantic model for prediction output
class PredictionOutput(BaseModel):
    weight: float

class TransactionModel(TransactionBase):
    id: int
    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
models.Base.metadata.create_all(bind=engine)

@app.post("/transactions/", response_model=TransactionModel)
async def create_transaction(transaction: TransactionBase, db: db_dependency):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.get("/transactions/", response_model=list[TransactionModel])
async def read_transactions(db: db_dependency, skip: int = 0, limit: int = 200):
    transactions = db.query(models.Transaction).all()
    return transactions

@app.put("/transactions/{transaction_id}", response_model=TransactionModel)
async def update_transaction(transaction_id: int, transaction: TransactionBase, db: db_dependency):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    for key, value in transaction.dict().items():
        setattr(db_transaction, key, value)

    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.delete("/transactions/{transaction_id}", response_model=TransactionModel)
async def delete_transaction(transaction_id: int, db: db_dependency):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(db_transaction)
    db.commit()
    return db_transaction

# Prediction endpoint
@app.post("/predict/", response_model=PredictionOutput)
async def predict(data: PredictionInput):
    # Prepare the data for prediction
    input_data = np.array([[data.height, data.men]])
    # Make the prediction
    predicted_weight = model.predict(input_data)
    return PredictionOutput(weight=predicted_weight)
