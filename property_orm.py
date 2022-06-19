from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import (
    Column,
    Integer,
    Float,
    Boolean,
    String,
    ForeignKey,
    create_engine,
    Enum,
)
from property import EnergyEfficiency

Base = declarative_base()


class Broker(Base):
    """An agent who manages the seller perspective."""

    __tablename__ = "BROKER"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)


class Property(Base):
    """A base class for rentals, houses for sales, etc."""

    # ToDo: add attributes which are non-primitive types
    __tablename__ = "PROPERTY"
    id = Column(Integer, primary_key=True)
    size = Column(Float)
    floor = Column(Integer)
    rooms = Column(Integer)
    year_of_construction = Column(Integer)
    is_furnished = Column(Boolean)
    is_kitchen_included = Column(Boolean)
    is_balcony_available = Column(Boolean)
    is_garden_available = Column(Boolean)
    energy_efficiency = Column(Enum(EnergyEfficiency))
    broker_id = Column(Integer, ForeignKey("BROKER.id"))
    broker = relationship("Broker", backref="properties")


if __name__ == "__main__":
    engine = create_engine("sqlite:///./properties_trading.db", echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    broker = Broker(first_name="Dagobert", last_name="Duck")
    session.add(broker)
    property_1 = Property(size=88.5, broker=broker)

    session.commit()
