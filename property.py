from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Dict
from abc import ABCMeta, abstractmethod


@dataclass
class Location:
    lat: float
    long: float
    city: str
    postal_code: str
    street: str
    street_number: str


class StatusFromTakerPerspective(Enum):
    bookmarked = 1
    contacted = 2
    appointment_scheduled = 3
    appointment_completed = 4
    closed = 5
    success = 6


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


@dataclass
class Property(metaclass=ABCMeta):
    id: int
    location: Location
    size: float
    floor: int
    rooms: int
    year_of_construction: int
    energy_efficiency: EnergyEfficiency
    is_furnished: bool
    is_kitchen_included: bool
    is_balcony_available: bool
    is_garden_available: bool


@dataclass
class Rental(Property):
    base_rent: float
    additional_costs: float

    @property
    def total_rent(self):
        return self.base_rent + self.additional_costs


@dataclass
class Actor(metaclass=ABCMeta):
    first_name: str
    last_name: str
    properties: Optional[List[Property]] = None

    def __post_init__(self):
        if self.properties is None:
            self.properties = []

    def add_property(self, new_property: Property):
        self.properties.append(new_property)


@dataclass
class Owner(Actor):
    pass


@dataclass
class Broker(Actor):
    pass


@dataclass
class Taker(Actor):
    property_stati: Optional[Dict[Property.id: StatusFromTakerPerspective]] = None

    def __post_init__(self):
        super().__post_init__()
        if self.property_stati is None:
            self.property_stati = [
                {property_id: StatusFromTakerPerspective.bookmarked for property_id in self.properties}]
        elif set(self.property_stati.keys()) != {property_.id for property_ in self.properties}:
            raise ValueError("The keys in property_stati must match the ids of properties exactly")

    def add_property(self, new_property: Property,
                     status: StatusFromTakerPerspective = StatusFromTakerPerspective.bookmarked):
        super().add_property(new_property)
        self.property_stati[new_property.id] = status
