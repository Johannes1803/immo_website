from enum import Enum

from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import (
    Column,
    Integer,
    Float,
    Boolean,
    String,
    ForeignKey,
    create_engine,
    Enum as SqlEnum,
)

Base: declarative_base = declarative_base()


class EnergyEfficiency(Enum):
    A_plus = 1
    A = 2
    B = 3
    C = 4
    D = 5
    E = 6
    F = 7
    G = 8
    H = 9


class AdStatus(Enum):
    created = 1
    online = 2
    not_taking_new_requests = 3
    taken = 4


class Agent(Base):
    """A base class for agents acting on properties."""

    __tablename__ = "agent"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    type = Column(String(20))

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "agent",
    }


class Broker(Agent):
    """An agent who manages the seller perspective."""

    __mapper_args__ = {
        "polymorphic_identity": "broker",
    }
    managed_properties = relationship("Property", back_populates="broker")


# class Taker(Agent):
#     """An agent who manages the potential taker perspective."""
#
#     __mapper_args__ = {
#         "polymorphic_identity": "taker",
#     }
#     watched_properties = relationship("Property", back_populates="agent")


class Property(Base):
    """A base class for rentals, houses for sale, etc."""

    __tablename__ = "property"
    id = Column(Integer, primary_key=True)
    size = Column(Float)
    floor = Column(Integer)
    rooms = Column(Integer)
    year_of_construction = Column(Integer)
    is_furnished = Column(Boolean)
    is_kitchen_included = Column(Boolean)
    is_balcony_included = Column(Boolean)
    is_garden_included = Column(Boolean)
    energy_efficiency = Column(SqlEnum(EnergyEfficiency))
    status = Column(SqlEnum(AdStatus), default=AdStatus.created)
    location = relationship("Location", back_populates="property", uselist=False)
    broker_id = Column(Integer, ForeignKey("agent.id"))
    broker = relationship("Broker", back_populates="managed_properties")
    type = Column(String(20))

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "property",
    }


class Rental(Property):
    base_rent = Column(Float)
    additional_costs = Column(Float)
    __mapper_args__ = {
        "polymorphic_identity": "rental",
    }


class Location(Base):
    """A location with address information."""

    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    lat = Column(Float)
    long = Column(Float)
    city = Column(String)
    postal_code = Column(String)
    street = Column(String)
    street_number = Column(String)
    property_id = Column(Integer, ForeignKey("property.id"))
    property = relationship("Property", back_populates="location", uselist=False)


if __name__ == "__main__":
    engine = create_engine("sqlite:///./properties_trading.db", echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    broker = Broker(first_name="Dagobert", last_name="Duck")
    session.add(broker)
    property_1 = Rental(
        size=88.5,
        floor=1,
        rooms=4,
        year_of_construction=10,
        is_furnished=False,
        is_kitchen_included=False,
        is_balcony_included=True,
        is_garden_included=True,
        energy_efficiency=EnergyEfficiency.B,
        broker=broker,
        base_rent=950.34,
        additional_costs=35.34,
    )
    session.add(property_1)

    location_1 = Location(
        lat=100.1,
        long=89.03,
        city="London",
        street="Downing Street",
        street_number="14b",
        postal_code="431",
        property=property_1,
    )
    session.add(location_1)

    property_2 = Rental(
        size=188.5,
        floor=2,
        rooms=4,
        year_of_construction=10,
        is_furnished=False,
        is_kitchen_included=False,
        is_balcony_included=True,
        is_garden_included=True,
        energy_efficiency=EnergyEfficiency.B,
        broker=broker,
        base_rent=950.34,
        additional_costs=35.34,
    )
    session.add(property_2)

    location_2 = Location(
        lat=90.1,
        long=89.03,
        city="London",
        street="Downing Street",
        street_number="14b",
        postal_code="431",
        property=property_2,
    )
    session.add(location_2)

    session.commit()

    for property_ in broker.managed_properties:
        print(property_.size)
