from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///test.db')
Base = declarative_base()
class Room(Base):
    __tablename__ = 'rooms'
    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    Surface_Area = Column(Float)
    Flooring_type = Column(String)
    Flooring_cost_per_sqft = Column(Float)
