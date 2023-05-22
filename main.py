from fastapi import FastAPI, HTTPException, Depends
import pandas as pd
from typing import List, Optional
from datetime import datetime, date
from sqlalchemy import or_, create_engine, Boolean, Column, ForeignKey, Integer, String, Date, Numeric, Float
from sqlalchemy.orm import relationship, Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel





app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    list_price = Column(Integer)
    close_price = Column(Integer)
    price_per_sqft = Column(Integer)
    sqft = Column(Integer)
    dom = Column(Integer)
    close_date = Column(Date)
    bathrooms = Column(Integer)
    bedrooms = Column(Integer)
    subdivision_name = Column(String)
    mls_major_area = Column(String)
    list_agent = Column(String)
    buyers_agent = Column(String)
    list_office_name = Column(String)
    buyer_office_name = Column(String)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class PropertyBase(BaseModel):
    id: int
    city: str
    address: str
    latitude: float
    longitude: float
    list_price: int
    close_price: int
    price_per_sqft: int
    sqft: int
    dom: int
    close_date: date
    bathrooms: Optional[int]
    bedrooms: int
    subdivision_name: Optional[str]
    mls_major_area: Optional[str]
    list_agent: str
    buyers_agent: str
    list_office_name: str
    buyer_office_name: str


    class Config:
        orm_mode = True

# read the CSV file into a DataFrame
df = pd.read_csv('properties.csv')

# create a session
db = SessionLocal()

# insert data into the database


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/properties/")
def read_properties(skip: int = 0, limit: int = 100):
    db = SessionLocal()
    properties = db.query(Property).offset(skip).limit(limit).all()
    return properties

@app.get("/properties/filter/", response_model=List[PropertyBase])
def filter_properties(query: str, db: Session = Depends(get_db)):
    properties = db.query(Property).filter(
        or_(
            Property.city.contains(query),
            Property.address.contains(query),
            Property.list_agent.contains(query),
            Property.buyers_agent.contains(query),
            Property.buyer_office_name.contains(query),
            Property.list_office_name.contains(query)
        )
    ).all()
    return properties

