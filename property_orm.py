from enum import Enum

from sqlalchemy.ext.associationproxy import association_proxy
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


class AdStatusTakerPerspective(Enum):
    watched = 1
    contacted = 2
    appointment_scheduled = 3
    rejected = 4
    accepted = 5


class AssociationTakerestate(Base):
    __tablename__ = "association_taker_estate"
    taker_id = Column(ForeignKey("agent.id"), primary_key=True)
    estate_id = Column(ForeignKey("estate.id"), primary_key=True)
    ad_status_taker_perspective = Column(SqlEnum(AdStatusTakerPerspective))
    estate = relationship("estate")

    def __init__(
        self,
        estate: "estate",
        ad_status_taker_perspective: AdStatusTakerPerspective,
    ):
        super().__init__()
        self.estate = estate
        self.ad_status_taker_perspective = ad_status_taker_perspective


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
    managed_properties = relationship("estate", back_populates="broker")


class Taker(Agent):
    """An agent who manages the potential taker perspective."""

    __mapper_args__ = {
        "polymorphic_identity": "taker",
    }
    _association_taker_properties = relationship("AssociationTakerestate")
    watched_properties = association_proxy(
        "_association_taker_properties",
        "estate",
        creator=lambda args: AssociationTakerestate(
            estate=args[0], ad_status_taker_perspective=args[1]
        ),
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class estate(Base):
    """A base class for rentals, houses for sale, etc."""

    __tablename__ = "estate"
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
    location = relationship("Location", back_populates="estate", uselist=False)
    broker_id = Column(Integer, ForeignKey("agent.id"))
    broker = relationship("Broker", back_populates="managed_properties")
    type = Column(String(20))

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "estate",
    }


class Rental(estate):
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
    estate_id = Column(Integer, ForeignKey("estate.id"))
    estate = relationship("estate", back_populates="location", uselist=False)


if __name__ == "__main__":
    engine = create_engine("sqlite:///./properties_trading.db", echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    broker = Broker(first_name="Dagobert", last_name="Duck")
    session.add(broker)
    estate_1 = Rental(
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
    session.add(estate_1)

    location_1 = Location(
        lat=100.1,
        long=89.03,
        city="London",
        street="Downing Street",
        street_number="14b",
        postal_code="431",
        estate=estate_1,
    )
    session.add(location_1)

    estate_2 = Rental(
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
    session.add(estate_2)

    location_2 = Location(
        lat=90.1,
        long=89.03,
        city="London",
        street="Downing Street",
        street_number="14b",
        postal_code="431",
        estate=estate_2,
    )
    session.add(location_2)

    taker = Taker(first_name="John", last_name="Doe")

    taker.watched_properties.append((estate_2, AdStatusTakerPerspective.rejected))
    session.add(taker)
    session.commit()

    for estate_ in taker.watched_properties:
        print(estate_)
