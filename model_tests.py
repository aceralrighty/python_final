import pytest

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Room, Supply, Base


@pytest.fixture(scope='module')
def test_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_calc_room(test_session):
    room = Room(
        name="A",
        Surface_Area=123,
        Flooring_type="Tile",
        Flooring_cost_per_sqft=300,
        tiling="None",
        tiling_cost_per_sqft=0,
        tiling_area=0,
    )
    test_session.add(room)
    test_session.commit()
    case = test_session.query(Room).filter_by(name="A").first()
    assert case.name == "A"
    assert case.Surface_Area == 123
    assert case.Flooring_type == "Tile"
    assert case.Flooring_cost_per_sqft == 300
    assert case.tiling == "None"
    assert case.tiling_cost_per_sqft == 0
    assert case.tiling_area == 0
    test_session.commit()

