from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Numeric, Computed
from sqlalchemy.orm import declarative_base, relationship

engine = create_engine('sqlite:///test.db')
Base = declarative_base()


class Room(Base):
    __tablename__ = 'rooms'
    Id = Column(Integer, primary_key=True)
    name = Column(String)
    Surface_Area = Column(Float)
    Flooring_type = Column(String)
    Flooring_cost_per_sqft = Column(Float)
    supply = relationship("supply", back_populates="rooms")

    def __repr__(self):
        return f"Name: {self.name}\nSurface Area: {self.Surface_Area}\n Flooring Type: {self.Flooring_type}\nFlooring per sqft Cost: {self.Flooring_cost_per_sqft}"


class Supply(Base):
    __tablename__ = 'supply'
    Id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.Id'))
    name = Column(String)
    quantity = Column(Integer)
    cost_per_item = Column(Float)
    total_supply_cost = Column(Numeric, Computed('quantity * cost_per_item'))

    rooms = relationship("rooms", back_populates="supply")

    def __repr__(self):
        return f"Name: {self.name}\nQuantity: {self.quantity}\nCost: {self.cost_per_item}\nTotal Supply Cost: {self.total_supply_cost}"