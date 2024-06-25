from database import Base
from sqlalchemy import Column, Integer, String, Float, Boolean

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    men = Column(Boolean)
    age = Column(Integer)
    height = Column(Float)
    #weight = Column(Float)

    



