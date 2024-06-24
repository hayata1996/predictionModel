#i will mdify this code into prediction app

from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated, List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
import models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost:3000",
    #"http://localhost:8000",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"]   # Allow all headers
)

#pydantic model
class TransactionBase(BaseModel):
    amount: float
    category: str
    description: str
    is_income: bool
    date: str
    
#grand son of pydantic model
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
#creating table, column... when the server starts
#

@app.post("/transactions/", response_model=TransactionModel)
async def create_transaction(transaction: TransactionBase, db: db_dependency):
    #this models.Transaction is the class in models.py, which defines the table with 6 columns
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.get("/transactions/", response_model=list[TransactionModel])
async def read_transactions(db: db_dependency, skip: int = 0, limit: int = 200):
    transactions = db.query(models.Transaction).all()
    return transactions

#under here is the codification today: 0622
#add delete and update function to the server
#originally written by GPT and modified by me
#return should include 6columns, 5 plus id column
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

