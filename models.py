from enum import Enum

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Numeric, Computed, SQLEnum
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine('sqlite:///supplies.db')
Base = declarative_base()


class TileType(Enum):
    CERAMIC = "Ceramic",
    PORCELAIN = "Porcelain",
    MARBLE = "Marble",
    GRANITE = "Granite",
    MOSAIC = "Mosaic",
    GLASS = "Glass",


class FloorType(Enum):
    HARDWOOD = "Hard Wood",
    TILE = "Tile",


class Room(Base):
    __tablename__ = 'rooms'
    Id = Column(Integer, primary_key=True)
    name = Column(String)
    Surface_Area = Column(Float)
    Flooring_type = Column(SQLEnum(FloorType))
    Flooring_cost_per_sqft = Column(Float)
    tiling = Column(SQLEnum(TileType))
    tiling_cost_per_sqft = Column(Float)
    tiling_area = Column(Float)
    supplies = relationship("supply", back_populates="rooms")

    def __repr__(self):
        return (f"Name: {self.name}\nSurface_Area: {self.Surface_Area}\nFlooring Type: {self.Flooring_type}\n"
                f"Flooring Cost: {self.Flooring_cost_per_sqft}\n"
                f"Tiling: {self.tiling}\n"
                f"Tiling Cost: {self.tiling_cost_per_sqft}\n"
                f"Tiling Area: {self.tiling_area}")

    def calc_cost(self):
        total_tile_cost = self.tiling_area * self.tiling_cost_per_sqft
        total_flooring_cost = self.Surface_Area * self.Flooring_cost_per_sqft
        total_supplies = sum(supply.total_supply_cost for supply in self.supplies)
        total_remodel_cost = total_flooring_cost + total_tile_cost + total_supplies


class Supply(Base):
    __tablename__ = 'supply'
    Id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.Id'))
    supply_name = Column(String)
    quantity = Column(Integer)
    cost_per_item = Column(Float)
    total_supply_cost = Column(Numeric, Computed('quantity * cost_per_item'))

    rooms = relationship("rooms", back_populates="supply")

    def __init__(self, supply_name, quantity, cost_per_item):
        self.supply_name = supply_name
        self.quantity = quantity
        self.cost_per_item = cost_per_item

    def __repr__(self):
        return f"Name: {self.supply_name}\nQuantity: {self.quantity}\nCost: {self.cost_per_item}\nTotal Supply Cost: {self.total_supply_cost}"


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
ss = Session()
